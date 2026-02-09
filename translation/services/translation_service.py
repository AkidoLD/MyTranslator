from translation.domain.models.translation_provider import TranslationRequest, TranslationProvider
from translation.domain.exceptions.translation_error import TranslationError
from translation.domain.models.translation_result import TranslationResult
from translation.domain.repositories.translation_provider_repository import TranslationProviderRepository
from translation.infra.factories.translation_provider_factory import TranslationProviderFactory


class TranslationService:
    def __init__(self, provider_repo : TranslationProviderRepository):
        if provider_repo is None or not isinstance(provider_repo, TranslationProviderRepository) :
            raise TypeError("The provider_repo must be type of TranslationProviderRepository. Actuel is " + str(type(provider_repo)))
        #
        self._provider_repo = provider_repo
        self._providers : dict[str, TranslationProvider] = {}
        self._active_provider : TranslationProvider | None = None
        #
        self._load_providers()

    def translate(self, text : str, target_lang : str, src_lang : str = "") -> TranslationResult:
        try :
            if not self.active_provider :
                raise ValueError("No active provider set on the translation service")
            #
            res = self.active_provider.translate(TranslationRequest(text, target_lang, src_lang))
            return TranslationResult(res.original, res.translated, res.target_lang, res.src_lang, res.details)
        #
        except TranslationError as e:
            raise RuntimeError("An error occurred during the translation", e)

    def _load_providers(self):
        self.providers = [TranslationProviderFactory.create_from_dict(repo) for repo in self._provider_repo.load()]

    def _save_providers(self):
        self._provider_repo.save([p.to_dict() for p in self.providers])

    def add_provider(self, provider : TranslationProvider):
        if not isinstance(provider, TranslationProvider) :
            raise TypeError("Translation provider must be type of TranslationAPI. The actual is ", type(provider))
        #
        if len(self._providers) == 0 : self._active_provider = provider
        #
        self._providers[provider.id] = provider
        #
        self._save_providers()

    def clear_provider(self):
        self._providers = {}

    @property
    def active_provider(self) -> TranslationProvider:
        return self._active_provider

    @active_provider.setter
    def active_provider(self, provider_id : str):
        self.set_active_provider(provider_id)

    def set_active_provider(self, provider_id):
        p = self._providers.get(provider_id)
        if not p :
            raise ValueError(f"The provider with the id {provider_id} isn't found")
        #
        self._active_provider = p

    @property
    def providers(self):
        return list(self._providers.values())

    @providers.setter
    def providers(self, providers : list[TranslationProvider]):
        if not isinstance(providers, list):
            raise TypeError("The 'providers' must be of type list. The actuel type is ", type(providers))
        #
        for item in providers : self.add_provider(item)
