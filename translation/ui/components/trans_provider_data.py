from dataclasses import dataclass


@dataclass
class TransProviderData:
    provider_id: str
    provider_name: str
    provider_type: str
    provider_lang_count: int = 0
    provider_req_internet: bool = True