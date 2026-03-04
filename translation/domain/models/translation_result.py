from dataclasses import dataclass


@dataclass
class TranslationResult :
    original: str
    translated: str
    src_lang: str
    target_lang: str
    details: dict