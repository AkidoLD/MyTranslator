from abc import ABC, abstractmethod
from typing import Optional

from translation.domain.enums.protocol import Protocol
from translation.domain.models.request import TranslationRequest
from translation.domain.models.response import TranslationResponse


class TranslationApi(ABC):
    """
    Abstract base class for any translation API implementation.

    Subclasses must specify:
    - which protocol they use (HTTP, file system, custom, etc.)
    - whether the API requires an internet connection
    - how the translation is executed internally
    """
    def __init__(self, name: str, required_internet: bool,protocol: Protocol, timeout : Optional[float] = None):
        if not isinstance(protocol, Protocol):
            raise TypeError("The 'protocol' must be type of Protocol")
        self.name = name
        self.required_internet = required_internet
        self.protocol = protocol
        self.timeout = timeout

    @abstractmethod
    def translate(self, request: TranslationRequest) -> TranslationResponse:
        """
        TranslateService the given request.

        Subclasses must:
        - perform the translation
        - return a TranslationResponse (never None)
        - never raise errors related to invalid input; encode them in the response instead

        :param request: TranslationRequest instance with the data to translate
        :return: TranslationResponse describing the outcome
        """
        pass

