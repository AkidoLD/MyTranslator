from typing import Optional


class TranslationResponse:
    """
    Represents the result returned by a translation API.

    A response always contains a success flag and optionally a translated text
    or an error message.
    """
    def __init__(self, status: bool, result: Optional[str] = None):
        """
        Create a TranslationResponse.

        :param status: True if the translation succeeded, False otherwise.
        :param result: The translated text when successful, otherwise
                       an error message describing the failure.
        """
        self.status = status
        self.result = result
