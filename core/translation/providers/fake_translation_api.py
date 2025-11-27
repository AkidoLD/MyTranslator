from core.translation.protocol import Protocol
from core.translation.request import TranslationRequest
from core.translation.response import TranslationResponse
from core.translation.translation_api import TranslationApi

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
