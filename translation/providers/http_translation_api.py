from translation.domain.enums.protocol import Protocol
from translation.domain.models.translation_api import TranslationApi


class HttpTranslationApi(TranslationApi):

    def __init__(
            self,
            name : str,
            timeout : float | None
    ):
        super().__init__(name, True ,Protocol.HTTP ,timeout)
