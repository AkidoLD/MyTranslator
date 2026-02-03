import subprocess
from subprocess import TimeoutExpired
from typing import Self


from translation.domain.exceptions.translation_error import TranslationError
from translation.domain.models.request import TranslationRequest
from translation.domain.models.response import TranslationResponse
from translation.domain.base.translation_api import TranslationApi
from translation.infra.enums import TranslationApiType


class ExecTranslationApi(TranslationApi):

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "req_internet": self.required_internet,
            "type": self.type,
            "langages": self.langages,
            "timeout": self.timeout,
            "binary": self._binary,
            "args": self._arguments,
            "lang_template": self._lang_template
        }

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        return ExecTranslationApi(
            data["id"],
            data["name"],
            data["binary"],
            data["args"],
            data["lang_template"],
            data["langages"],
            data["req_internet"],
            data["timeout"]
        )

    def __init__(
            self,
            api_id: str | None,
            name: str,
            binary: str,
            arguments: dict,
            lang_template: str,
            langages: dict = None,
            req_internet: bool = True,
            timeout: float = 5
    ):
        """
        Create a translation provider based on executing a command-line tool.

        :param name: Name of this translation API.
        :param binary: Path or name of the executable binary to run.
        :param arguments: A dictionary representing the CLI arguments to insert
                          into the command. Keys are flags, values are parameters.
        :param lang_template: A template used to generate the language pair.
                                 `_current` is replaced with the input language,
                                 `_target` with the target language.

            Example:
                >>> api = ExecTranslationApi(
                        "abcdef",
                ...     "translate",
                ...     "trans",
                ...     {"-b": ""},
                ...     "_current:_target",
                ... )

            When calling translate(), the command executed will look like:
                trans -b fr:en text
        """

        if not isinstance(arguments, dict):
            raise TypeError("The 'arguments' argument must be a dictionary")

        super().__init__(api_id, name, req_internet, TranslationApiType.EXEC, langages, timeout)

        self._binary = binary
        self._arguments = arguments
        self._lang_template = lang_template
        self._timeout = timeout

    def translate(self, request: TranslationRequest) -> TranslationResponse:
        """
        Executes the CLI translation tool and returns the translation result.
        """

        # Build the language argument by replacing placeholders
        lang_spec = self._lang_template.replace("_current", request.source_lang) \
            .replace("_target", request.target_lang)

        # Build command safely using a list
        command = [self._binary]

        # Add CLI arguments from the dictionary
        for flag, value in self._arguments.items():
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
        except FileNotFoundError | TimeoutExpired as e:
            raise TranslationError("An error occurred during the translation", e)

        # If the process failed (non-zero exit code)
        if process.returncode != 0:
            raise TranslationError("The translation process failed on ExecTranslationApi")

        # Success
        result = process.stdout.strip()
        return TranslationResponse(
            request.source_lang,
            result,
            request.target_lang,
            request.source_lang,
            {
                "Langue source": request.source_lang,
                "Langue destinataire": request.target_lang,
                "Texte": request.text,
                "Traduction": result,
            }
        )
