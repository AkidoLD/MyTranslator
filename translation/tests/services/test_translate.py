from unittest import TestCase

from translation.services.translateservice import TranslateService
from translation.providers.fake_translation_api import FakeTranslationApi


class TestTranslate(TestCase):

    def setUp(self):
        provider = FakeTranslationApi()
        self.translate = TranslateService(provider)

    def test_trans_returns_valid_response(self):
        response = self.translate.trans("salut", "en")
        self.assertEqual(response, "salut")

    def test_trans_raises_runtime_error_on_invalid_request(self):
        with self.assertRaises(RuntimeError):
            self.translate.trans("", "en")

    def test_provider_setter_updates_provider(self):
        old_provider = self.translate.provider
        self.translate.provider = FakeTranslationApi()
        self.assertNotEqual(old_provider, self.translate.provider)

    def test_provider_getter_returns_current_provider(self):
        current_provider = self.translate.provider
        self.assertEqual(current_provider, self.translate.provider)

    def test_provider_setter_raises_type_error_if_invalid(self):
        with self.assertRaises(TypeError) as context:
            self.translate.provider = ""
        self.assertEqual(str(context.exception), "The 'provider' must be of type TranslationApi")
