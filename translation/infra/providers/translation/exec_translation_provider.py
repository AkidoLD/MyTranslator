import re
import subprocess
from subprocess import TimeoutExpired
from typing import Self

from translation.domain.exceptions.translation_error import TranslationError, ProviderUnavailableError, \
    TranslationTimeOutError
from translation.domain.models.translation_request import TranslationRequest
from translation.domain.models.translation_response import TranslationResponse
from translation.domain.models.translation_provider import TranslationProvider
from translation.infra.enums.translation_provider_type import TranslationProviderType


class ExecTranslationProvider(TranslationProvider):
    #Mappable keys
    KEY_BINARY = "binary"
    KEY_ARGS = "args"
    KEY_LANG_TEMPLATE = "lang_template"

    #
    _SRC_LANG_TEMPLATE = "@src_lang"
    _TARGET_LANG_TEMPLATE = "@target_lang"

    #
    _BLACKLISTED_BINARIES = {
        "rm", "mkfs", "dd", "fdisk", "shred", "wipefs",
        "shutdown", "reboot", "halt", "poweroff",
        "chmod", "chown", "chroot", "sudo", "su",
    }

    def __init__(
            self,
            provider_id: str | None,
            name: str,
            binary: str,
            arguments: dict,
            lang_template: str,
            languages: dict = None,
            req_internet: bool = True,
            detect_src_lang: bool = False,
            timeout: float = 5.0
    ):
        """
        Create a translation provider based on executing a command-line tool.

        :param name: Name of this translation API.
        :param binary: Path or _name_lb of the executable binary to run.
        :param arguments: A dictionary representing the CLI arguments to insert
                          into the command. Keys are flags, values are parameters.
        :param lang_template: A template used to generate the language pair.
                                 `_current` is replaced with the input language,
                                 `_target` with the target language.

            Example:
                >>> api = ExecTranslationProvider(,
                        None,
                ...     "Translate",
                ...     "trans",
                ...     {"-b": ""},
                ...     "@src_lang:@target_lang",
                        {...},
                        True,
                        10.0
                ... )

            When calling translate(), the command executed will look like:
                trans -b fr:en text
        """
        super().__init__(provider_id, name, req_internet, languages, detect_src_lang, timeout)

        self.binary = binary
        self.arguments = arguments
        self.lang_template = lang_template

    @property
    def binary(self):
        return self._binary

    @binary.setter
    def binary(self, value: str):
        if not isinstance(value, str):
            raise TypeError(f"binary must be str, got {type(value).__name__}")

        value = value.strip()

        if not value:
            raise ValueError("Provider binary cannot be empty")

        if not re.match(r'^[a-zA-Z0-9/_\-.]+$', value):
            raise ValueError(f"Provider binary contains invalid characters: {value}")
        #
        binary_name = value.split("/")[-1]
        if binary_name in self._BLACKLISTED_BINARIES:
            raise ValueError(f"Binary '{binary_name}' is not allowed for security reasons.")

        self._binary = value

    @property
    def arguments(self):
        return self._arguments

    @arguments.setter
    def arguments(self, value: dict):
        if not isinstance(value, dict):
            raise TypeError(f"argument must be dictionary, got _type {type(value).__name__}")
        #
        self._arguments = value

    @property
    def lang_template(self):
        return self._lang_template

    @lang_template.setter
    def lang_template(self, value: str):
        if not isinstance(value, str):
            raise ValueError(f"lang_template must be string, got _type {type(value).__name__}")
        #
        if self._SRC_LANG_TEMPLATE not in value:
            raise ValueError(f"lang_template must contain {self._SRC_LANG_TEMPLATE} to identify src language")
        #
        if self._TARGET_LANG_TEMPLATE not in value:
            raise ValueError(f"lang_template must contain {self._TARGET_LANG_TEMPLATE} to identify target language")
        #
        self._lang_template = value

    def translate(self, request: TranslationRequest) -> TranslationResponse:
        """
        Executes the CLI translation tool and returns the translation result.
        """

        # Build the language argument by replacing placeholders
        lang_spec = self.lang_template.replace(self._SRC_LANG_TEMPLATE, request.source_lang) \
            .replace(self._TARGET_LANG_TEMPLATE, request.target_lang)

        # Build command safely using a list
        command = [self.binary]

        # Add CLI arguments from the dictionary
        for flag, value in self.arguments.items():
            command.append(flag)
            if value:
                command.append(value)

        # Add language specifier
        command.append(lang_spec)

        # Finally add the text to translate
        command.append(request.text)

        try:
            # Execute the command and capture output
            process = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=self._timeout,
            )
        #
        except FileNotFoundError as e:
            raise ProviderUnavailableError(f"Provider binary not found. Check at {self.binary} if it exist.", e)

        except  TimeoutExpired as e:
            raise TranslationTimeOutError(f"translation timeout exceeded.", e)

        if process.returncode != 0:
            raise TranslationError(f"Translation process must end with code 0, got code {process.returncode}")

        # Success
        result = process.stdout.strip()
        return TranslationResponse(
            request.text,
            result,
            request.source_lang or "auto",
            request.target_lang,
            {
                "Langue source": request.source_lang or "auto",
                "Langue destinataire": request.target_lang,
                "Texte": request.text,
                "Traduction": result,
            }
        )

    def to_dict(self) -> dict:
        return {
            self.KEY_ID: self.id,
            self.KEY_NAME: self.name,
            self.KEY_BINARY: self.binary,
            self.KEY_TYPE: self.type,
            self.KEY_ARGS: self.arguments,
            self.KEY_LANG_TEMPLATE: self.lang_template,
            self.KEY_REQ_INTERNET: self.req_internet,
            self.KEY_LANGUAGES: self.languages,
            self.KEY_DETECT_SRC_LANG: self.detect_src_lang,
            self.KEY_TIMEOUT: self.timeout
        }

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        return ExecTranslationProvider(
            data.get(cls.KEY_ID, None),
            data.get(cls.KEY_NAME, ""),
            data.get(cls.KEY_BINARY, ""),
            data.get(cls.KEY_ARGS, {}),
            data.get(cls.KEY_LANG_TEMPLATE, ""),
            data.get(cls.KEY_LANGUAGES, {}),
            data.get(cls.KEY_REQ_INTERNET, True),
            data.get(cls.KEY_DETECT_SRC_LANG, False),
            data.get(cls.KEY_TIMEOUT, 5.0)
        )

    def get_type(self) -> str:
        return TranslationProviderType.EXEC
