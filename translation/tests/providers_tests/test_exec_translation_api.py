from unittest import TestCase

from translation.infra.providers.translation.exec_translation_provider import ExecTranslationProvider
from translation.domain.models.translation_request import TranslationRequest


class TestExecTranslationProvider(TestCase):
    def setUp(self):
        name = "Trans"
        binary = "/home/akido-ld/.local/bin/trans"
        args = {"-b": ""}
        lang_templ = "_current:_target"
        langages = {
            "francais" : "fr",
            "anglais" : "en",
            "espagnol" : "es"
        }
        #
        self.provider = ExecTranslationProvider(None, name, binary, args, lang_templ, langages, True, 3)

    def test_exec_translation_api_work(self):
        self.provider._binary = "/home/akido-ld/.local/bin/trans"
        response = self.provider.translate(TranslationRequest("Hello", "fr", "en"))
        self.assertIsNotNone(response.translated)
        self.assertEqual("Bonjour", response.translated)

    def test_exec_translation_api_return_the_error_when_the_status_is_false(self):
        self.provider._binary = "not_a_binary"
        response = self.provider.translate(TranslationRequest("test", "en"))
        self.assertIsNotNone(response.translated)
