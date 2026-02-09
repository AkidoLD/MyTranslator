import time
import uuid
from abc import ABC
from datetime import datetime, timezone

from shared.domain.interfaces.mappable import Mappable


class HistoryEntryData(Mappable, ABC):
    def __init__(self, provider_key : str, entry_id : str = None, entry_time : datetime = None):
        self.module_name = provider_key
        self.id = entry_id or str(uuid.uuid4())
        self.time = entry_time or datetime.now(timezone.utc)