from typing import List, Dict, Any, Iterable

from history.domain.interfaces.history_repository import HistoryRepository


class FakeHistoryRepository(HistoryRepository):

    def __init__(self):
        self._data_map: Dict[str, str | None | Dict[str, Any]] = {}
        self._history_map: Dict[str, List] = {}
        self._data_map["history"] = self._history_map
        self._data_map["active_provider"] = None
        #

    def get_active_provider(self) -> str:
        return self._data_map["active_provider"]

    def add_history(self, data: dict):
        key = data.get("provider_key")
        #
        if not self._history_map.get(key): self._history_map[key] = []
        self._history_map[key].append(data)

    def delete_history_by_id(self, history_id: str):
        for h in self.get_all_history() :
            if h.get("id") != history_id : self.add_history(h)

    def provider_history_count(self, provider_key: str) -> int:
        return len([value for value in self.get_all_history() if value.get("provider_key") == provider_key])

    def count_all_history(self) -> int:
        return sum(len(p) for p in self._history_map.values())

    def provider_history_is_empty(self, provider_key) -> bool:
        return not self._history_map[provider_key]

    def history_is_empty(self) -> bool:
        return not self._history_map

    def get_provider_history(self, provider_key: str, offset: int = 0, limit: int | None = None) -> List[Dict]:
        _offset = offset
        _history_count = self.provider_history_count(provider_key)
        limit = limit if limit is not None else _history_count
        _limit = min(limit + _offset, _history_count)
        #
        history = self._history_map.get(provider_key, [])
        return history[_offset:_limit]

    def get_all_history(self, offset: int = 0, limit: int | None = None) -> List[Dict]:
        return [item for p in self._history_map.values() for item in p]
