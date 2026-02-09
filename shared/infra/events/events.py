from enum import StrEnum


class Events(StrEnum):
    # Translation
    TRANSLATION_STARTED = "translation.started"
    TRANSLATION_COMPLETED = "translation.completed"
    TRANSLATION_FAILED = "translation.failed"

    # History
    HISTORY_ENTRY_ADDED = "history.entry_added"
    HISTORY_ENTRY_DELETED = "history.entry_deleted"
