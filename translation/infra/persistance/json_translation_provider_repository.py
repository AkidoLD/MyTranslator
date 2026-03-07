from typing import Dict, Any, Iterable, List

from shared.infra.interfaces.json_repository import JsonRepository
from shared.infra.utils.validation_utils import validate_type
from translation.domain.exceptions.translation_repository_exception import (
    ProviderDataUpdateFailed, TranslationProviderNotFound, InvalidRepositoryDataFormat)
from translation.domain.models.translation_provider import TranslationProvider
from translation.domain.repositories.translation_provider_repository import TranslationProviderRepository


class JsonTranslationProviderRepository(TranslationProviderRepository, JsonRepository):

    _PROVIDERS_KEY = "provider_list"
    _ACTIVE_PROVIDER_KEY = "active_provider"
    #

    def __init__(self, path: str):
        super().__init__(path)
        #

    def delete(self, provider_id : str):
        data = self.get_all()
        providers = [provider for provider in data.get(self._PROVIDERS_KEY)
                     if provider.get_provider(TranslationProvider.KEY_ID) != provider_id]
        #
        data[self._PROVIDERS_KEY] = providers
        if data.get(self._ACTIVE_PROVIDER_KEY) == provider_id : data[self._ACTIVE_PROVIDER_KEY] = None
        #
        self.save(data)

    def exist(self, provider_id : str):
        return any(provider_id for p in self.get_providers() if p.get(TranslationProvider.KEY_ID, "") == provider_id)

    def len(self) -> int:
        return sum(1 for _ in self.get_providers())

    def clear(self):
        self.save({})

    def add(self, provider_data: Dict[str, Any]):
        if not isinstance(provider_data, dict) :
            raise InvalidRepositoryDataFormat(f"provider data must be dict, got {type(provider_data).__name__}")
        #
        _data = self.get_providers()
        _data.append(provider_data)
        #
        self.save_providers(_data)

    def get_provider(self, provider_id: str) -> Dict[str, Any] | None:
        validate_type(provider_id, str, "provider_id")
        #
        for data in self.get_providers():
            if data.get(TranslationProvider.KEY_ID) == provider_id : return data
            #
        return None

    def get_provider_by(self, attr_name: str, value) -> Iterable[Dict[str, Any]]:
        for p_data in self.get_providers():
            if attr_name not in p_data : return #Exit if the attribut not exist
            if p_data.get(attr_name) == value :
                yield p_data

    def find_provider_by_name(self, provider_name: str) -> Iterable[Dict[str, Any]]:
        return (p_data for p_data in self.get_providers() if provider_name.lower() in p_data.get(TranslationProvider.KEY_NAME, "").lower())

    def get_all(self) -> Dict[str, Any]:
        repositories = self.load()
        if repositories and not isinstance(repositories, dict) :
            raise InvalidRepositoryDataFormat(f"Repository data format must be dict, got {type(repositories).__name__}")
        #
        return repositories or {}

    def update(self, provider_id: str, changes: Dict[str, Any]):
        if not self.exist(provider_id) :
            raise ProviderDataUpdateFailed(f"No provider with id {provider_id} found")
        #
        data = []
        for _p_data in self.get_providers():
            if _p_data.get(TranslationProvider.KEY_ID) == provider_id :
                for k, v in changes.items() : _p_data[k] = v
            #
            data.append(_p_data)
        #
        self.save_providers(data)

    def get_active_provider(self) -> str | None:
        return self.get_all().get(self._ACTIVE_PROVIDER_KEY)

    def set_active_provider(self, provider_id: str):
        if provider_id is not None and not self.exist(provider_id):
            raise TranslationProviderNotFound(f"No provider with id {provider_id} found.")
        #
        data = self.get_all()
        data[self._ACTIVE_PROVIDER_KEY] = provider_id
        #
        self.save(data)

    def get_providers(self) -> list[dict]:
        return self.get_all().get(self._PROVIDERS_KEY, [])

    def save_providers(self, providers : List[Dict[str, Any]]):
        data = self.get_all()
        data[self._PROVIDERS_KEY] = validate_type(providers, list, "providers")
        #
        self.save(data)
