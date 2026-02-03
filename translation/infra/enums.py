from enum import Enum, StrEnum


class TranslationApiType(StrEnum):
    EXEC = "exec",
    HTTP = "http",
    LIB = "lib"