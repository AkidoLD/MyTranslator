class TranslationError(Exception):
    pass

class TranslationTimeOutError(TranslationError):
    pass

class ProviderUnavailableError(TranslationError):
    pass

class UnsupportedLanguageError(TranslationError):
    pass