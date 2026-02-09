from datetime import datetime
from typing import Self

from history.domain.interfaces.history_entry_data import HistoryEntryData
from translation.infra.integration.history.constants import TRANS_PROVIDER_KEY


class TranslationHistoryEntry(HistoryEntryData):
    #Dictionary keys
    KEY_ENTRY_ID = "id"
    KEY_PROVIDER_KEY = "provider_key"
    KEY_ORIGINAL_TEXT = "original_text"
    KEY_TRANSLATED_TEXT = "translated_text"
    KEY_SRC_LANG = "src_lang"
    KEY_TARGET_LANG = "target_lang"
    KEY_ENTRY_TIME = "time"
    #
    def __init__(self, entry_id : str | None, original_text : str, translated_text : str, src_lang : str, target_lang : str, entry_time : datetime | None):
        super().__init__(TRANS_PROVIDER_KEY, entry_id, entry_time)
        #
        self.original_text = original_text
        self.translated_text = translated_text
        self.src_lang = src_lang
        self.target_lang = target_lang
        
    def to_dict(self) -> dict:
        return {
            self.KEY_ENTRY_ID : self.id,
            self.KEY_PROVIDER_KEY : self.module_name,
            self.KEY_ORIGINAL_TEXT : self.original_text,
            self.KEY_TRANSLATED_TEXT : self.translated_text,
            self.KEY_SRC_LANG : self.src_lang,
            self.KEY_TARGET_LANG : self.target_lang,
            self.KEY_ENTRY_TIME : self.time.timestamp()
        }

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        return cls(
            data.get(cls.KEY_ENTRY_ID),
            data.get(cls.KEY_ORIGINAL_TEXT),
            data.get(cls.KEY_TRANSLATED_TEXT),
            data.get(cls.KEY_SRC_LANG),
            data.get(cls.KEY_TARGET_LANG),
            datetime.fromtimestamp(data.get(cls.KEY_ENTRY_TIME))
        )


if __name__ == "__main__" :
    t = TranslationHistoryEntry(None, "Salut bro", "Hello Broo", "fr", "en", None)
    #
    m = t.to_dict()
    n = TranslationHistoryEntry.from_dict(m)
    print(m, n.id)
