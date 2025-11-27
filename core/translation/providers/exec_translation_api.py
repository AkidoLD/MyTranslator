import copy
import subprocess
from subprocess import TimeoutExpired
from typing import Optional

from core.translation.protocol import Protocol
from core.translation.request import TranslationRequest
from core.translation.response import TranslationResponse
from core.translation.translation_api import TranslationApi


class ExecTranslationApi(TranslationApi):

    def __init__(
            self,
            name: str,
            binary: str,
            arguments: dict,
            lang_template: str,
            timeout: Optional[float] = None
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
                ...     "translate",
                ...     "trans",
                ...     {"-b": ""},
                ...     "_current:_target"
                ... )

            When calling translate(), the command executed will look like:
                trans -b fr:en text
        """

        if not isinstance(arguments, dict):
            raise TypeError("The 'arguments' argument must be a dictionary")

        super().__init__(name, False, Protocol.EXEC)

        self._binary = binary
        self._arguments = arguments
        self._lang_template = lang_template
        self._timeout = timeout

    def translate(self, request: TranslationRequest) -> TranslationResponse:
        """
        Executes the CLI translation tool and returns the translation result.
        """

        # Build the language argument by replacing placeholders
        lang_spec = self._lang_template.replace("_current", request.source_lang)\
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
                timeout=self._timeout
            )
        except FileNotFoundError:
            return TranslationResponse(False, "Binary not found")
        except TimeoutExpired:
            return TranslationResponse(False, "Translation timeout pass")

        # If the process failed (non-zero exit code)
        if process.returncode != 0:
            return TranslationResponse(False, process.stderr.strip())

        # Success
        result = process.stdout.strip()
        return TranslationResponse(True, result)


