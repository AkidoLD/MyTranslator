from abc import ABC, abstractmethod
from typing import List, Dict


class HistoryRepository(ABC):

    @abstractmethod
    def get_active_provider_key(self) -> str | None:
        pass

    @abstractmethod
    def add_history(self, data : dict):
        pass

    @abstractmethod
    def add_history_list(self,  history_list : List[Dict]):
        pass

    @abstractmethod
    def delete_history_by_id(self, history_id : str):
        pass

    @abstractmethod
    def count_history_by_provider(self, provider_key : str) -> int:
        pass

    @abstractmethod
    def count_all_history(self) -> int:
        pass

    @abstractmethod
    def history_of_provider_is_empty(self, provider_key) -> bool:
        pass

    @abstractmethod
    def history_is_empty(self) -> bool:
        pass

    @abstractmethod
    def get_history_by_provider(self, provider_key : str, offset : int = 0, limit : int | None = None) -> List[Dict]:
        pass

    @abstractmethod
    def get_all_history(self, offset : int = 0, limit : int | None = None) -> List[Dict]:
        pass