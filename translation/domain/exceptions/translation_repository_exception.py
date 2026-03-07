

class TranslationRepositoryException(Exception):
    pass

class TranslationProviderNotFound(TranslationRepositoryException):
    pass

class ProviderDataUpdateFailed(TranslationRepositoryException):
    pass