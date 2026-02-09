from typing import Self

from translation.domain.models.translation_provider import TranslationProvider
from translation.domain.models.translation_request import TranslationRequest
from translation.domain.models.translation_response import TranslationResponse


class LibTranslationProvider(TranslationProvider):
    def translate(self, request: TranslationRequest) -> TranslationResponse:
        pass

    def to_dict(self) -> dict:
        pass

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        pass