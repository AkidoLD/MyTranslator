from dataclasses import dataclass


@dataclass
class TranslationResult :
    original: str
    translated: str
    target_lang: str
    src_lang: str
    details: dict