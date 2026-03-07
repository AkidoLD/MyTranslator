from typing import Self

from translation.domain.exceptions.translation_error import TranslationError
from translation.domain.models.translation_request import TranslationRequest
from translation.domain.models.translation_response import TranslationResponse
from translation.domain.models.translation_provider import TranslationProvider
from translation.infra.enums.translation_provider_type import TranslationProviderType


class FakeTranslationProvider(TranslationProvider):
    def to_dict(self) -> dict:
        return {
            self.KEY_ID: self.id,
            self.KEY_NAME: self.name,
            self.KEY_TYPE: self.type,
            self.KEY_REQ_INTERNET: self.req_internet,
            self.KEY_LANGUAGES: self.languages,
            self.KEY_DETECT_SRC_LANG: self.detect_src_lang,
            self.KEY_TIMEOUT: self.timeout
        }

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        return cls (
            data.get(cls.KEY_ID, None),
            data.get(cls.KEY_NAME, ""),
            data.get(cls.KEY_REQ_INTERNET, False),
            data.get(cls.KEY_LANGUAGES, {}),
            data.get(cls.KEY_DETECT_SRC_LANG, False),
            data.get(cls.KEY_TIMEOUT, 5.0)
        )

    def __init__(
            self,
            provider_id: str | None,
            name: str,
            req_internet: bool,
            languages : dict[str, str],
            detect_src_lang : bool,
            timeout : float
    ):
        super().__init__(provider_id, name, req_internet, languages, detect_src_lang, timeout)

    def translate(self, request: TranslationRequest) -> TranslationResponse:
        if not request.text:
            raise TranslationError("An error occurred during the translation. No text to translate.")
        #
        return TranslationResponse(
            request.text,
            "fake text",
            request.source_lang,
            request.target_lang,
            {
                f"Faux de details N {i}" : f"details {i}" for i in range(1, 5)
            }
        )

    def get_type(self) -> str:
        return TranslationProviderType.FAKE