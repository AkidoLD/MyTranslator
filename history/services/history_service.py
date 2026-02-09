from typing import Dict, List

from history.domain.interfaces.history_entry_data import HistoryEntryData
from history.domain.interfaces.history_provider import HistoryProvider
from history.domain.interfaces.history_repository import HistoryRepository
from shared.infra.events.event_bus import event_bus
from shared.infra.events.events import Events


class HistoryService :
    def __init__(
            self,
            repository : HistoryRepository,
            providers : List[HistoryProvider] | None = None
    ):
        if not isinstance(repository, HistoryRepository) :
            raise TypeError(f"The repository must be type of HistoryRepository. The actual is {type(repository)}")
        #
        self._repository = repository
        self._providers : Dict[str, HistoryProvider] = {}
        self._active_provider : HistoryProvider | None = None
        self.providers = providers or []

    def add_provider(self, provider : HistoryProvider):
        if not isinstance(provider, HistoryProvider) :
            raise TypeError(f"The provider must be type of HistoryProvider. The actual is {type(provider)}")
        #
        if provider.provider_key.strip() == "":
            raise ValueError("The key can't be empty.")
        #
        self._providers[provider.provider_key] = provider

    @property
    def providers(self) -> List[HistoryProvider]:
        return list(p for p in self._providers.values())

    @providers.setter
    def providers(self, values : List[HistoryProvider]):
        if not isinstance(values, list):
            raise TypeError(f"The value must be type of dict. The actual is {type(values)}")
        #
        for provider in values:
            self.add_provider(provider)

    def set_active_provider(self, provider_key : str):
        provider = self._providers.get(provider_key)
        if not provider :
            raise ValueError(f"The provider with the key : {provider_key} has not found.")
        #
        self._active_provider = provider

    @property
    def active_provider(self):
        return self._active_provider

    @property
    def repository(self):
        return self._repository

    def add_history_entry(self, history_entry : HistoryEntryData):
        self.repository.add_history(history_entry.to_dict())
        event_bus.publish(Events.HISTORY_ENTRY_ADDED, history_entry)

    def add_history_entry_list(self, history_list : List[HistoryEntryData]):
        self.repository.add_history_list([data.to_dict() for data in history_list])

    def get_active_provider_history(self, offset : int = 0, limit : int |  None = None) -> List[HistoryEntryData]:
        if not self.active_provider :
            raise RuntimeError("No active_provider set.")
        #
        return self.get_provider_history(self.active_provider, offset, limit)

    def get_provider_history_count(self, provider : HistoryProvider):
        if not isinstance(provider, HistoryProvider):
            raise TypeError(f"The provider must be type of HistoryProvider. The Actual is {type(provider)}")
        #
        return self.repository.count_history_by_provider(provider.provider_key)

    def get_all_history_count(self):
        return self.repository.count_all_history()

    def get_provider_history(self, provider : HistoryProvider, offset : int = 0, limit : int |  None = None):
        if not isinstance(provider, HistoryProvider) :
            raise TypeError(f"The provider must be type of HistoryProvider. The Actual is {type(provider)}")
        #
        datas = self.repository.get_history_by_provider(provider.provider_key, offset, limit)
        #
        return [provider.deserialize_entry_data(data) for data in datas]

    def get_all_providers_history(self):
        history = []
        for p in self.providers : history.extend(self.get_provider_history(p))
        #
        return history