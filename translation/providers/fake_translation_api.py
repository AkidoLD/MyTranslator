from translation.domain.enums.protocol import Protocol
from translation.domain.models.request import TranslationRequest
from translation.domain.models.response import TranslationResponse
from translation.domain.models.translation_api import TranslationApi

class FakeTranslationApi(TranslationApi):
    def __init__(self):
        super().__init__(
            name="Fake API",
            required_internet=False,
            protocol=Protocol.EXEC
        )

    def translate(self, request: TranslationRequest) -> TranslationResponse:
        if not request.text:
            return TranslationResponse(status=False, result=None)
        return TranslationResponse(status=True, result=request.text)
