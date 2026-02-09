from dataclasses import dataclass, field


@dataclass
class TranslationResponse:
    """Represents the result returned by a translation API."""
    original : str
    translated : str
    target_lang : str
    src_lang : str = ""
    details : dict = field(default_factory = dict)