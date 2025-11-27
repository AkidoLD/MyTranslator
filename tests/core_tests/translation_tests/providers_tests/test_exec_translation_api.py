from http.client import responses
from unittest import TestCase

from core.translation.providers.exec_translation_api import ExecTranslationApi
from core.translation.request import TranslationRequest


class TestExecTranslationApi(TestCase):
    def setUp(self):
        name = "Trans"
        binary = "/home/akido-ld/.local/bin/trans"
        args = {"-b": ""}
        lang_templ = "_current:_target"

        self.provider = ExecTranslationApi(name, binary, args, lang_templ, 3)

    def test_exec_translation_api_work(self):
        self.provider._binary = "/home/akido-ld/.local/bin/trans"
        response = self.provider.translate(TranslationRequest("Hello", "fr", "en"))
        self.assertTrue(response.status)
        self.assertEqual("Bonjour", response.result)

    def test_exec_translation_api_return_the_error_when_the_status_is_false(self):
        self.provider._binary = "not_a_binary"
        response = self.provider.translate(TranslationRequest("test", "en"))
        self.assertFalse(response.status)
        self.assertEqual('Binary not found', response.result)
