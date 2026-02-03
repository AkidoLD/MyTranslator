from typing import Self

from translation.domain.base.translation_api import TranslationApi
from translation.domain.models.request import TranslationRequest
from translation.domain.models.response import TranslationResponse


class LibTranslationApi(TranslationApi):
    def translate(self, request: TranslationRequest) -> TranslationResponse:
        pass

    def to_dict(self) -> dict:
        pass

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        pass