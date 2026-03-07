from abc import ABC, abstractmethod
from typing import List, Dict, Iterable


class HistoryRepository(ABC):

    @abstractmethod
    def get_active_provider_key(self) -> str | None:
        pass

    @abstractmethod
    def add_history(self, data : dict):
        pass

    @abstractmethod
    def delete_history_by_id(self, history_id : str):
        pass

    @abstractmethod
    def provider_history_count(self, provider_key : str) -> int:
        pass

    @abstractmethod
    def count_all_history(self) -> int:
        pass

    @abstractmethod
    def provider_history_is_empty(self, provider_key) -> bool:
        pass

    @abstractmethod
    def history_is_empty(self) -> bool:
        pass

    @abstractmethod
    def get_provider_history(self, provider_key : str, offset : int = 0, limit : int | None = None) -> List[Dict]:
        pass

    @abstractmethod
    def get_all_history(self, offset : int = 0, limit : int | None = None) -> List[Dict]:
        pass