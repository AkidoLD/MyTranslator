from abc import ABC, abstractmethod
from typing import List, Dict, Iterable


class HistoryRepository(ABC):
    #-- CRUD Methods -------------------------
    @abstractmethod
    def get(self, entry_id) -> dict | None : pass

    @abstractmethod
    def get_all(self, offset: int = 0, limit: int | None = None) -> Iterable[dict]: pass

    @abstractmethod
    def add(self, entry_data : dict): pass

    @abstractmethod
    def delete(self, entry_id): pass

    @abstractmethod
    def exist(self, entry_id) -> bool : pass

    @abstractmethod
    def count(self) -> int : pass

    @abstractmethod
    def empty(self) -> bool : pass

    def __len__(self): return self.count()

    #-- Provider Methods --------------------
    @abstractmethod
    def get_by_provider(self, provider_key : str,  offset: int = 0, limit: int | None = None) -> Iterable[dict]: pass

    @abstractmethod
    def get_provider_count(self, provider_key : str) -> int: pass

    @abstractmethod
    def provider_is_empty(self, provider_key) -> bool: pass