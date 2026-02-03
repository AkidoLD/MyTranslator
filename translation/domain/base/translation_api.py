import uuid
from abc import ABC, abstractmethod
from typing import Self, Dict

from translation.domain.models.request import TranslationRequest
from translation.domain.models.response import TranslationResponse
from translation.infra.enums import TranslationApiType


class TranslationApi(ABC):
    """
    Abstract base class for any translation API implementation.

    Subclasses must specify:
    - which protocol they use (HTTP, file system, custom, etc.)
    - whether the API requires an internet connection
    - how the translation is executed internally
    """
    def __init__(self,api_id : str | None,  name: str, required_internet: bool, api_type: TranslationApiType, langages : dict = None, timeout : float = 5):
        if not isinstance(api_type, TranslationApiType):
            raise TypeError("The 'protocol' must be type of Protocol")
        self.id = api_id or str(uuid.uuid4())
        self.name = name
        self.required_internet = required_internet
        self.type = api_type
        self.langages = langages or Dict[str, str]
        self.timeout = timeout

    @abstractmethod
    def translate(self, request: TranslationRequest) -> TranslationResponse:
        """
        TranslationService the given request.

        Subclasses must:
        - perform the translation
        - return a TranslationResponse (never None)

        :param request: TranslationRequest instance with the data to translate
        :return: TranslationResponse describing the outcome
        :raise TranslationError if the translation failed
        """
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        """Convert this object to a dictionary structure"""
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, data : dict) -> Self :
        pass


