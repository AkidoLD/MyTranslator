import uuid
from abc import ABC, abstractmethod
from typing import Dict

from shared.domain.interfaces.mappable import Mappable
from translation.domain.models.translation_request import TranslationRequest
from translation.domain.models.translation_response import TranslationResponse


class TranslationProvider(Mappable, ABC):
    #Mappable interface keys
    KEY_ID = "id"
    KEY_NAME = "name"
    KEY_TYPE = "type"
    KEY_REQ_INTERNET = "req_internet"
    KEY_DETECT_SRC_LANG = "detect_src_lang"
    KEY_LANGUAGES = "languages"
    KEY_TIMEOUT = "timeout"

    """
    Abstract base class for any translation provider implementation.

    Subclasses must specify:
    - which provider _type they use (HTTP, exec, lib, ...)
    - whether the provider requires an internet connection
    - how the translation is executed internally
    """

    def __init__(
            self,
            provider_id: str | None,
            name: str,
            req_internet: bool,
            languages: Dict[str, str] | None = None,
            detect_src_lang : bool = False,
            timeout: float = 5.0
    ):
        self.id = provider_id or str(uuid.uuid4())
        self.name = name
        self.req_internet = req_internet
        self.languages = languages or {}
        self.detect_src_lang = detect_src_lang
        self.timeout = timeout

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, value : str):
        if not isinstance(value, str) :
            raise TypeError(f"id must be string, got _type {type(value).__name__}.")
        #
        if not value.strip() :
            raise ValueError("Provider id cannot be empty.")
        #
        self._id = value

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value : str):
        if not isinstance(value, str):
            raise TypeError(f"name must be string, gt type {type(value).__name__}.")
        if not value.strip():
            raise ValueError("Provider name cannot be empty.")
        #
        self._name = value

    @property
    def type(self):
        return self.get_type()

    @property
    def req_internet(self) -> bool:
        return self._req_internet

    @req_internet.setter
    def req_internet(self, value : bool):
        if not isinstance(value, bool):
            raise TypeError(f"req_internet must be boolean, got type {type(value).__name__}.")
        #
        self._req_internet = value

    @property
    def languages(self) -> Dict[str, str]:
        return self._languages

    @languages.setter
    def languages(self, value : Dict[str, str]):
        if not isinstance(value, dict):
            raise TypeError(f"languages must be dict, got type {type(value).__name__}")
        #
        self._languages = value

    @property
    def detect_src_lang(self):
        return self._detect_src_lang
        
    @detect_src_lang.setter
    def detect_src_lang(self, value : bool):
        if not isinstance(value, bool) :
            raise TypeError(f"detect_src_lang must be bool, got type {type(value).__name__}")
        #
        self._detect_src_lang = value
        
    @property
    def timeout(self) -> float:
        return self._timeout

    @timeout.setter
    def timeout(self, value : float):
        if not isinstance(value, (int, float)):
            raise TypeError(f"timeout must be numeric, got {type(value).__name__}")
        #
        if value <= 0:
            raise ValueError(f"Timeout must be positive, got {value}")
        #
        self._timeout = float(value)

    @abstractmethod
    def translate(self, request: TranslationRequest) -> TranslationResponse:
        """
        Translate the given request.

        Subclasses must:
        - perform the translation
        - return a TranslationResponse (never None)

        :param request: TranslationRequest instance with the data to translate
        :return: TranslationResponse describing the outcome
        :raises TranslationProviderError: if the translation failed
        """
        pass

    @abstractmethod
    def get_type(self) -> str:
        pass