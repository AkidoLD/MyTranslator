from unittest import TestCase

from translation.infra.persistance.fake_translation_provider_repository import FakeTranslationApiRepository
from translation.services.translation_service import TranslationService
from translation.infra.providers.translation.fake_translation_provider import FakeTranslationApi


class TestTranslate(TestCase):

    def setUp(self):
        provider = FakeTranslationApi("Fake Babana")
        self.translate = TranslationService(FakeTranslationApiRepository())

    def test_trans_returns_valid_response(self):
        response = self.translate.translate("salut", "en", "fr")
        self.assertEqual(response, "salut")

    def test_trans_raises_runtime_error_on_invalid_request(self):
        with self.assertRaises(RuntimeError):
            self.translate.translate("", "en")

    def test_provider_setter_updates_provider(self):
        old_provider = self.translate.provider
        self.translate.provider = FakeTranslationApi("Fake Babana")
        self.assertNotEqual(old_provider, self.translate.provider)

    def test_provider_getter_returns_current_provider(self):
        current_provider = self.translate.active_provider
        self.assertEqual(current_provider, self.translate.active_provider)

    def test_provider_setter_raises_type_error_if_invalid(self):
        with self.assertRaises(TypeError) as context:
            self.translate.provider = ""
        self.assertEqual(str(context.exception), "The 'provider' must be of _type TranslationApi")
