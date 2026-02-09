import uuid
from abc import ABC, abstractmethod
from typing import Dict

from shared.domain.interfaces.mappable import Mappable
from translation.domain.models.translation_request import TranslationRequest
from translation.domain.models.translation_response import TranslationResponse
from translation.domain.enums.translation_provider_type import TranslationProviderType


class TranslationProvider(Mappable, ABC):
    """
    Abstract base class for any translation API implementation.

    Subclasses must specify:
    - which provider type they use (HTTP, file system, custom, etc.)
    - whether the API requires an internet connection
    - how the translation is executed internally
    """
    def __init__(self, provider_id : str | None, name: str, required_internet: bool, provider_type: TranslationProviderType, langages : dict = None, timeout : float = 5):
        if not isinstance(provider_type, TranslationProviderType):
            raise TypeError("The 'protocol' must be type of Protocol")
        self.id = provider_id or str(uuid.uuid4())
        self.name = name
        self.required_internet = required_internet
        self.type = provider_type
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