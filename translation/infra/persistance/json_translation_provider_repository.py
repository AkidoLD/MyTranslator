import json
from pathlib import Path
from typing import Dict, Any, Iterable, List

from shared.infra.utils.validation_utils import validate_type
from translation.domain.exceptions.translation_repository_exception import (
    ProviderDataUpdateFailed, TranslationRepositoryException, TranslationProviderNotFound)
from translation.domain.models.translation_provider import TranslationProvider
from translation.domain.repositories.translation_provider_repository import TranslationProviderRepository


class JsonTranslationProviderRepository(TranslationProviderRepository):

    _PROVIDERS_KEY = "provider_list"
    _ACTIVE_PROVIDER_KEY = "active_provider"
    #

    def __init__(self, file_path: str):
        self.file_path = file_path

    @property
    def file_path(self):
        return str(self._file_path.absolute())

    @file_path.setter
    def file_path(self,  path : str):
        f = Path(path)
        if not f.exists() : f.touch()
        self._file_path = f

    def _load(self) -> dict[str, dict | str]:
        try :
            with self._file_path.open("r") as file :
                data = json.load(file)
                if not isinstance(data, dict) :
                    raise TranslationRepositoryException("Invalid JSON format. Expected format is dict")
                #
                return data
        except (RuntimeError, ValueError, TranslationRepositoryException) as e :
            raise TranslationRepositoryException(f"Failed to load data : {e}")

    def _save(self, data: dict[str, dict]):
        try :
            with self._file_path.open("w") as file :
                json.dump(data, file, indent=2)
        #
        except (RuntimeError, ValueError, TranslationRepositoryException, TypeError) as e:
            raise TranslationRepositoryException(f"Failed to save data : {e}")

    def _load_providers(self) -> Iterable[dict]:
        return self._load().get(self._PROVIDERS_KEY, [])

    def _save_providers(self, providers : List[Dict[str, Any]]):
        data = self._load()
        data[self._PROVIDERS_KEY] = validate_type(providers, list, "providers")
        #
        self._save(data)

    def delete(self, provider_id : str):
        providers = [provider for provider in self._load_providers()
                     if provider.get(TranslationProvider.KEY_ID, "") != provider_id]
        #
        self._save_providers(providers)

    def exist(self, provider_id : str):
        return any(provider_id for p in self._load_providers() if p.get(TranslationProvider.KEY_ID, "") == provider_id)

    def len(self) -> int:
        return sum(1 for _ in self._load_providers())

    def clear(self):
        self._save_providers([])

    def add(self, provider_data: Dict[str, Any]):
        _data = list(self._load_providers())
        _data.append(provider_data)
        self._save_providers(_data)

    def get(self, provider_id: str) -> Dict[str, Any] | None:
        for data in self._load_providers() :
            if data.get(TranslationProvider.KEY_ID) == provider_id : return data
            #
        return None

    def get_by(self, attr_name: str, value) -> Iterable[Dict[str, Any]]:
        _data = []
        for p_data in self._load_providers() :
            if attr_name not in p_data : return #Exit if the attribut not exist
            if p_data.get(attr_name) == value :
                yield p_data

    def find_by_name(self, provider_name: str) -> Iterable[Dict[str, Any]]:
        return (p_data for p_data in self._load_providers() if provider_name.lower() in p_data.get(TranslationProvider.KEY_NAME, "").lower())

    def get_all(self) -> Iterable[Dict[str, Any]]:
        return self._load_providers()

    def update(self, provider_id: str, changes: Dict[str, Any]):
        if not self.exist(provider_id) :
            raise ProviderDataUpdateFailed(f"No provider with id {provider_id} found")
        #
        data = []
        for _p_data in self._load_providers() :
            if _p_data.get(TranslationProvider.KEY_ID) == provider_id :
                for k, v in changes.items() : _p_data[k] = v
            #
            data.append(_p_data)
        #
        self._save_providers(data)

    def get_active_provider(self) -> Dict[str, Any] | None:
        return self.get(self._load().get(self._ACTIVE_PROVIDER_KEY))

    def set_active_provider(self, provider_id: str):
        if not self.exist(provider_id):
            raise TranslationProviderNotFound(f"No provider with id {provider_id} found.")
        #
        data = self._load()
        data[self._ACTIVE_PROVIDER_KEY] = provider_id
        #
        self._save(data)

