from typing import Optional


class TranslationRequest:
    """
    Represents a request made to a translation API.

    It encapsulates all necessary information to translate a word or sentence
    from a source language to a target language.
    """
    def __init__(self, text: str, target_lang: str, source_lang: str = ""):
        """
        Create a TranslationRequest.

        :param text: The text to translate.
        :param target_lang: The target language code (e.g. 'en', 'fr').
        :param source_lang: Optional source language code. If None, the API
                            implementation may attempt to auto-detect it.
        """
        self.text = text
        self.source_lang = source_lang
        self.target_lang = target_lang
