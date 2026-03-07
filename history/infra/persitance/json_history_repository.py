

from history.domain.exceptions.history_repository_exception import InvalidDataFormatException
from history.domain.interfaces.history_entry_data import HistoryEntryData
from history.domain.interfaces.history_repository import HistoryRepository
from shared.infra.interfaces.json_repository import JsonRepository


class JsonHistoryRepository(JsonRepository, HistoryRepository):
    def __init__(self, path):
        super().__init__(path)
        #

    def get_all(self, offset: int = 0, limit: int | None = None) -> list[dict]:
        entries =  self.load()
        if entries and not isinstance(entries, list) :
            raise InvalidDataFormatException(f"Repository data format is invalid, got {type(entries).__name__} instead of list")
        #
        return entries[offset : offset + limit if limit is not None else None] if entries else []

    def get(self, entry_id) -> dict | None:
        for entry in self.get_all() :
            if entry.get(HistoryEntryData.KEY_ENTRY_ID) == entry_id :
                return entry
            #
        return None

    def add(self, entry_data: dict):
        if not isinstance(entry_data, dict):
            raise InvalidDataFormatException(f"Entry data format is invalid, got {type(entry_data).__name__} instead of dict")
        #
        entries = self.get_all()
        entries.append(entry_data)
        #
        self.save(entries)

    def delete(self, entry_id):
        self.save(entry for entry in self.get_all() if entry.get(HistoryEntryData.KEY_ENTRY_ID) != entry_id)

    def exist(self, entry_id) -> bool:
        return any(entry for entry in self.get_all() if entry.get(HistoryEntryData.KEY_ENTRY_ID) == entry_id)

    def count(self) -> int:
        return len(self.get_all())

    def empty(self) -> bool:
        return not any(self.get_all())

    def get_by_provider(self, provider_key: str, offset: int = 0, limit: int | None = None) -> list[dict]:
        return [entry for entry in self.get_all()
                if entry.get(HistoryEntryData.KEY_PROVIDER_KEY, "") == provider_key][offset : None if limit is None else offset + limit]

    def get_provider_count(self, provider_key: str) -> int:
        return sum(1 for _ in self.get_by_provider(provider_key))

    def provider_is_empty(self, provider_key) -> bool:
        return not any(self.get_by_provider(provider_key))

