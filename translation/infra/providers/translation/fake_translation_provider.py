from typing import Self

from translation.domain.exceptions.translation_error import TranslationError
from translation.domain.models.translation_request import TranslationRequest
from translation.domain.models.translation_response import TranslationResponse
from translation.domain.models.translation_provider import TranslationProvider
from translation.domain.enums.translation_provider_type import TranslationProviderType


class FakeTranslationProvider(TranslationProvider):
    def to_dict(self) -> dict:
        return {
            "name" : self.name,
            "type" : self.type
        }

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        return cls (data.get("name", ""))

    def __init__(self, name : str):
        super().__init__(
            None,
            name,
            False,
            TranslationProviderType.FAKE,
            {
                "francais" : "fr",
                "anglais" : "en"
            }
        )

    def translate(self, request: TranslationRequest) -> TranslationResponse:
        if not request.text:
            raise TranslationError("An error occurred during the translation")
        return TranslationResponse(
            "faux text",
            "fake text",
            "fr",
            "en",
            {
                f"Faux de details N {i}" : f"details {i}" for i in range(1, 10)
            }
        )
