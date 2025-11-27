from core.translation.protocol import Protocol
from core.translation.translation_api import TranslationApi


class HttpTranslationApi(TranslationApi):

    def __init__(
            self,
            name : str,
            timeout : float | None
    ):
        super().__init__(name, True ,Protocol.HTTP ,timeout)
