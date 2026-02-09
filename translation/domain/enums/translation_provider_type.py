from enum import StrEnum


class TranslationProviderType(StrEnum):
    EXEC = "exec",
    HTTP = "http",
    LIB = "lib",
    FAKE = "fake"