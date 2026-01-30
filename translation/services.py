from typing import Optional
from translation.domain.models.translation_api import TranslationApi, TranslationRequest, TranslationResponse

class TranslateService:
    def __init__(self, provider: TranslationApi):
        self.provider = provider

    def trans(
        self,
        text: str,
        target_lang: str,
        current_lang: Optional[str] = None
    ) -> str:
        request = TranslationRequest(text, target_lang, current_lang)
        response = self._provider.translate(request)
        if not response.status:
            raise RuntimeError(f"The translation failed: {response.result}")
        return response.result

    @property
    def provider(self):
        return self._provider

    @provider.setter
    def provider(self, provider: TranslationApi):
        if not isinstance(provider, TranslationApi):
            raise TypeError("The 'provider' must be of type TranslationApi")
        self._provider = provider
