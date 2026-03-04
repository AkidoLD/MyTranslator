from enum import StrEnum


class TranslationEvents(StrEnum):
    COMPLETED = "translation.completed"
    FAILED = "translation.failed"
    STARTED = "translation.started"
    PROVIDER_CHANGED = "translation.provider.changed"

class HistoryEvents(StrEnum):
    ENTRY_ADDED = "history.entry.added"
    ENTRY_DELETED = "history.entry.deleted"
    ENTRY_UPDATED = "history.entry.updated"
    PROVIDER_CHANGED = "history.provider.changed"