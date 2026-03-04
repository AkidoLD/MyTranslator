from dataclasses import asdict

from shared.infra.events.event_bus import event_bus
from shared.infra.events.events import TranslationEvents
from translation.domain.models.translation_provider import TranslationRequest, TranslationProvider
from translation.domain.exceptions.translation_error import TranslationTimeOutError, \
    ProviderUnavailableError, UnsupportedLanguageError, TranslationError
from translation.domain.models.translation_result import TranslationResult
from translation.domain.repositories.translation_provider_repository import TranslationProviderRepository
from translation.infra.factories.translation_provider_factory import TranslationProviderFactory
from translation.services.exceptions.translation_service_exception import NoActiveProviderError, \
    LoadProviderFailedError, SaveProviderFailedError


class TranslationService:
    def __init__(self, provider_repo : TranslationProviderRepository):
        if provider_repo is None or not isinstance(provider_repo, TranslationProviderRepository) :
            raise TypeError(f"Provider repository must be TranslationProviderRepository, got type {type(provider_repo).__name__}")
        #
        self._provider_repo = provider_repo
        self._providers : dict[str, TranslationProvider] = {}
        self._active_provider : TranslationProvider | None = None
        #
        self._load_providers()

    def translate(self, text : str, target_lang : str, src_lang : str = "") -> TranslationResult:
        try :
            if not self.active_provider :
                raise NoActiveProviderError("No active provider set on the translation service")
            #
            response = self.active_provider.translate(TranslationRequest(text, target_lang, src_lang))

            #Publish event
            event_bus.publish(TranslationEvents.COMPLETED, asdict(response))
            #
            return TranslationResult(response.original, response.translated, response.src_lang, response.target_lang, response.details)
        #
        except (TranslationTimeOutError, ProviderUnavailableError, UnsupportedLanguageError) :
            event_bus.publish(TranslationEvents.FAILED, {})
            raise
        except TranslationError :
            event_bus.publish(TranslationEvents.FAILED, {})
            raise

    def _load_providers(self):
        try :
            for provider in [TranslationProviderFactory.create_from_dict(repo) for repo in self._provider_repo.load()]:
                self.add_provider(provider)
        except RuntimeError as e :
            raise LoadProviderFailedError(f"Failed to load providers : {str(e)}")

    def _save_providers(self):
        try :
            self._provider_repo.save([p.to_dict() for p in self.providers])
        except RuntimeError as e :
            raise SaveProviderFailedError(f"Failed to save providers : {str(e)}")

    def add_provider(self, provider : TranslationProvider):
        if not isinstance(provider, TranslationProvider) :
            raise TypeError(f"Translation provider must be TranslationProvider, got type {type(provider).__name__}")
        #
        if len(self._providers) == 0 : self._active_provider = provider
        #
        self._providers[provider.id] = provider
        #
        self._save_providers()

    def remove_provider(self, provider_id):
        self._provider_repo.delete(provider_id)
        self._load_providers()

    def provider_exist(self, provider_id):
        self._provider_repo.exist(provider_id)

    def get_provider(self, provider_id):
        self._load_providers()
        #
        for p in self.providers:
            if p.id ==provider_id : return p
        #
        return None

    def clear_provider(self):
        self._providers = {}
        self._active_provider = None

    @property
    def active_provider(self) -> TranslationProvider:
        return self._active_provider

    @active_provider.setter
    def active_provider(self, provider_id : str):
        self.set_active_provider(provider_id)

    def set_active_provider(self, provider_id):
        provider = self._providers.get(provider_id)
        if not provider :
            raise ValueError(f"The provider with the id {provider_id} isn't found")
        #
        self._active_provider = provider
        #
        event_bus.publish(TranslationEvents.PROVIDER_CHANGED, {"provider_id" : provider_id})

    @property
    def providers(self):
        return list(self._providers.values())

    @providers.setter
    def providers(self, providers : list[TranslationProvider]):
        if not isinstance(providers, list):
            raise TypeError(f"providers must be list, got type {type(providers).__name__}.")
        #
        self.clear_provider()
        for item in providers : self.add_provider(item)
