from tkinter import Misc

from history.domain.interfaces.history_entry_data import HistoryEntryData
from history.domain.interfaces.history_entry_widget import HistoryEntryWidget
from history.domain.interfaces.history_provider import HistoryProvider
from translation.infra.integration.history.constants import TRANS_PROVIDER_KEY
from translation.infra.integration.history.translation_history_entry import TranslationHistoryEntry
from translation.infra.integration.history.translation_history_widget import TranslationHistoryWidget


class TranslationHistoryProvider(HistoryProvider):
    def __init__(self):
        super().__init__(TRANS_PROVIDER_KEY, "Traduction")

    def deserialize_entry_data(self, data: dict) -> HistoryEntryData:
        return TranslationHistoryEntry.from_dict(data)

    def create_entry_widget(self, master: Misc, entry_data: TranslationHistoryEntry) -> HistoryEntryWidget:
        if not isinstance(entry_data, TranslationHistoryEntry) :
            raise TypeError(f"The entry_data must be type of TranslationHistoryEntry. The actual is {type(entry_data)}")
        #

        return TranslationHistoryWidget(
            master,
            entry_data.original_text,
            entry_data.translated_text,
            entry_data.src_lang,
            entry_data.target_lang,
            entry_data.time
        )