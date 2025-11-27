from enum import StrEnum

class Protocol (StrEnum):
    HTTP = "http"
    SSH = "ssh"
    EXEC = 'exec'
    LIB = 'library'