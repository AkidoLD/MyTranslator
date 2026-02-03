from translation.domain.models.request import TranslationRequest
from translation.domain.models.response import TranslationResponse
from translation.domain.base.translation_api import TranslationApi
from translation.infra.enums import TranslationApiType


class HttpTranslationApi(TranslationApi):

    def translate(self, request: TranslationRequest) -> TranslationResponse:
        pass

    def __init__(
            self,
            name : str,
            timeout : float | None
    ):
        super().__init__(name, True ,TranslationApiType.HTTP ,timeout)
