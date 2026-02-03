from dataclasses import dataclass


@dataclass
class TranslationRequest:
    """
    Represents a request made to a translation API.

    It encapsulates all necessary information to translate a word or sentence
    from a source language to a target language.
    """
    text : str
    target_lang: str
    source_lang : str = ""
