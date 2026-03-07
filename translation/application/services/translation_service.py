from dataclasses import asdict
from typing import Any, Dict, Iterable

from shared.infra.events.event_bus import event_bus
from shared.infra.events.events import TranslationEvents
from shared.infra.utils.validation_utils import validate_type
from translation.domain.models.translation_provider import TranslationRequest, TranslationProvider
from translation.domain.exceptions.translation_error import TranslationError
from translation.domain.models.translation_result import TranslationResult
from translation.domain.repositories.translation_provider_repository import TranslationProviderRepository
from translation.application.factories.translation_provider_factory import TranslationProviderFactory
from translation.application.services.exceptions.translation_service_exception import NoActiveProviderError


class TranslationService:
    TRANS_COMPLETED = "translation.completed"
    TRANS_FAILED = "translation.failed"
    TRANS_STARTED = "translation.started"
    #
    TRANS_PROVIDER_ADDED = "translation.provider.added"
    TRANS_PROVIDER_REMOVED = "translation.provider.removed"
    TRANS_PROVIDER_CHANGED = "translation.provider.changed"
    TRANS_PROVIDER_UPDATE = "translation.provider.update"
    TRANS_PROVIDER_CLEAR = "translation.provider.clear"
    #

    def __init__(self, provider_repo : TranslationProviderRepository):
        if provider_repo is None or not isinstance(provider_repo, TranslationProviderRepository) :
            raise TypeError(f"Provider repository must be TranslationProviderRepository, got type {type(provider_repo).__name__}")
        #
        self._provider_repo = provider_repo

    def translate(self, text : str, target_lang : str, src_lang : str = "") -> TranslationResult:
        try :
            if not self.active_provider :
                raise NoActiveProviderError("No active provider set on the translation service")
            #
            response = self.active_provider.translate(TranslationRequest(text, target_lang, src_lang))

            #Publish event
            event_bus.publish(self.TRANS_COMPLETED, asdict(response))
            #
            return TranslationResult(response.original, response.translated, response.src_lang, response.target_lang, response.details)
        #
        except (RuntimeError, TranslationError ) as e:
            event_bus.publish(self.TRANS_FAILED, {"error_msg" : str(e)})
            raise e

    def add_provider(self, provider : TranslationProvider):
        validate_type(provider, TranslationProvider, "provider")
        self._provider_repo.add(provider.to_dict())
        event_bus.publish(self.TRANS_PROVIDER_ADDED, {TranslationProvider.KEY_ID : provider.id})

    def remove_provider(self, provider_id):
        self._provider_repo.delete(provider_id)
        event_bus.publish(self.TRANS_PROVIDER_REMOVED, {TranslationProvider.KEY_ID : provider_id})

    def provider_exist(self, provider_id):
        self._provider_repo.exist(provider_id)

    def get_provider(self, provider_id) -> TranslationProvider:
        provider_data = self._provider_repo.get_provider(provider_id)
        return TranslationProviderFactory.create_from_dict(provider_data) if provider_data else None

    def update_provider(self, provider_id : str, changes : Dict[str, Any]):
        self._provider_repo.update(provider_id, changes)
        event_bus.publish(self.TRANS_PROVIDER_UPDATE, {TranslationProvider.KEY_ID : provider_id})

    def find_provider_by_name(self, name : str) -> Iterable[TranslationProvider]:
        return [TranslationProviderFactory.create_from_dict(provider)
                for provider in self._provider_repo.find_provider_by_name(name)]

    def clear_provider(self):
        self._provider_repo.clear()
        event_bus.publish(self.TRANS_PROVIDER_UPDATE, {})

    @property
    def active_provider(self) -> TranslationProvider | None:
        p_id = self._provider_repo.get_active_provider()
        if not p_id : return None
        return TranslationProviderFactory.create_from_dict(self._provider_repo.get_provider(p_id))

    @active_provider.setter
    def active_provider(self, provider_id : str):
        self._provider_repo.set_active_provider(provider_id)
        event_bus.publish(TranslationEvents.PROVIDER_CHANGED, {"provider_id": provider_id})

    @property
    def providers(self):
        return [TranslationProviderFactory.create_from_dict(provider)
                for provider in self._provider_repo.get_providers()]

    @providers.setter
    def providers(self, providers : list[TranslationProvider]):
        for provider in validate_type(providers, list, "providers") :
            self.add_provider(provider)