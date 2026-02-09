from typing import Self

from translation.domain.models.translation_request import TranslationRequest
from translation.domain.models.translation_response import TranslationResponse
from translation.domain.models.translation_provider import TranslationProvider
from translation.domain.enums.translation_provider_type import TranslationProviderType


class HttpTranslationProvider(TranslationProvider):

    def to_dict(self) -> dict:
        pass

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        pass

    def translate(self, request: TranslationRequest) -> TranslationResponse:
        pass

    def __init__(
            self,
            name : str,
            req_internet,
            langages,
            timeout : float | None
    ):
        super().__init__(None, name, req_internet, TranslationProviderType.HTTP, langages, timeout)
