from abc import ABC, abstractmethod
from tkinter import Misc

from history.domain.interfaces.history_entry_data import HistoryEntryData
from history.domain.interfaces.history_entry_widget import HistoryEntryWidget


class HistoryProvider(ABC):
    PROVIDER_KEY = "provider_key"
    #

    def __init__(self, title : str):
        self._title = title

    @property
    def title(self):
        return self._title

    @property
    def provider_key(self):
        return self.get_key()

    @staticmethod
    @abstractmethod
    def get_key() -> str : pass

    @abstractmethod
    def deserialize_entry_data(self, data : dict) -> HistoryEntryData:
        pass

    @abstractmethod
    def create_entry_widget(self, master : Misc, entry_data : HistoryEntryData) -> HistoryEntryWidget:
        pass