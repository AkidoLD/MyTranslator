from abc import ABC, abstractmethod
from typing import Any, Dict, Iterable


class TranslationProviderRepository(ABC):
    @abstractmethod
    def get_active_provider(self) -> Dict[str, Any] | None : pass

    @abstractmethod
    def set_active_provider(self, provider_id : str) : pass

    @abstractmethod
    def add(self, provider_data : Dict[str, Any]): pass

    @abstractmethod
    def get(self, provider_id : str) -> Dict[str, Any] | None: pass

    @abstractmethod
    def get_by(self, attr_name : str, value) -> Iterable[Dict[str, Any]]: pass

    @abstractmethod
    def find_by_name(self, provider_name : str) -> Iterable[Dict[str, Any]] : pass

    @abstractmethod
    def get_all(self) -> Iterable[Dict[str, Any]]: pass

    @abstractmethod
    def update(self, provider_id : str, changes : Dict[str, Any]): pass

    @abstractmethod
    def delete(self, provider_id: str): pass

    @abstractmethod
    def exist(self, provider_id: str): pass

    @abstractmethod
    def len(self) -> int: pass

    def is_empty(self) -> bool:
        return not any(self.get_all())

    @abstractmethod
    def clear(self): pass

