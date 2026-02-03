from translation.domain.base.translation_api import TranslationApi, TranslationRequest
from translation.domain.exceptions.translation_error import TranslationError
from translation.domain.models.result import TranslationResult


class TranslationService:
    def __init__(self, providers: list[TranslationApi] = None):
        self._providers : dict[str, TranslationApi] = {}
        self._active_provider : TranslationApi | None = None
        #
        self.providers = providers or []

    def translate(self, text : str, target_lang : str, src_lang : str = "") -> TranslationResult:
        try :
            if not self.active_provider :
                raise ValueError("No active provider set on the translation service")
            #
            res = self.active_provider.translate(TranslationRequest(text, target_lang, src_lang))
            return TranslationResult(res.original, res.translated, res.target_lang, res.src_lang, res.details)
        except TranslationError as e:
            raise RuntimeError("An error occurred during the translation", e)

    def add_provider(self, api : TranslationApi):
        if not isinstance(api, TranslationApi) :
            raise TypeError("Translation provider must be type of TranslationAPI. The actual is ", type(api))
        #
        if len(self._providers) == 0 : self._active_provider = api
        #
        self._providers[api.id] = api

    def clear_provider(self):
        self._providers = {}

    @property
    def active_provider(self) -> TranslationApi:
        return self._active_provider

    @active_provider.setter
    def active_provider(self, provider_id : str):
        self.set_active_provider(provider_id)

    def set_active_provider(self, provider_id):
        p = self._providers.get(provider_id)
        print(f"New provider select. ID = {provider_id}")
        if not p :
            raise ValueError(f"The provider with the id {provider_id} isn't found")
        #
        self._active_provider = p

    @property
    def providers(self):
        return self._providers

    @providers.setter
    def providers(self, providers : list[TranslationApi]):
        if not isinstance(providers, list):
            raise TypeError("The 'providers' must be of type list. The actuel type is ", type(providers))
        #
        for item in providers : self.add_provider(item)
