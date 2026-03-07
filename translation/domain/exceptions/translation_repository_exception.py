

class TranslationRepositoryException(Exception):
    pass

class InvalidRepositoryDataFormat(TranslationRepositoryException):
    pass

class TranslationProviderNotFound(TranslationRepositoryException):
    pass

class ProviderDataUpdateFailed(TranslationRepositoryException):
    pass