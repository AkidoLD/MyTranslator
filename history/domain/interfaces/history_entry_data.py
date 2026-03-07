import time
import uuid
from abc import ABC, abstractmethod
from datetime import datetime, timezone

from shared.domain.interfaces.mappable import Mappable


class HistoryEntryData(Mappable, ABC):
    KEY_ENTRY_ID = "entry_id"
    KEY_ENTRY_TIME = "entry_time"
    KEY_PROVIDER_KEY = "provider_key"
    #

    def __init__(self, entry_id : str = None, entry_time : datetime = None):
        self.id = entry_id or str(uuid.uuid4())
        self.time = entry_time or datetime.now(timezone.utc)

    @staticmethod
    @abstractmethod
    def get_key() -> str : pass

    @property
    def provider_key(self):
        return self.get_key()