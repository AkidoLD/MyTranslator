class TranslationServiceError(Exception):
    pass

class NoActiveProviderError(TranslationServiceError):
    pass

class LoadProviderFailedError(TranslationServiceError):
    pass

class SaveProviderFailedError(TranslationServiceError):
    pass
