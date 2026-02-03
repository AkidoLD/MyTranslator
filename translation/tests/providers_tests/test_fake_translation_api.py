# tests/test_fake_translation_api.py

from unittest import TestCase
from translation.infra.providers.fake_translation_api import FakeTranslationApi
from translation.domain.base.translation_api import TranslationRequest
from translation.domain.enums.protocol import Protocol


class TestFakeTranslationApi(TestCase):

    def setUp(self):
        self.provider = FakeTranslationApi()

    def test_object_initialization(self):
        self.assertEqual(self.provider.name, "Fake API")
        self.assertEqual(self.provider.protocol, Protocol.EXEC)

    def test_translation_returns_valid_response(self):
        response = self.provider.translate(TranslationRequest("Salut", "eng"))
        self.assertTrue(response.status)
        self.assertEqual(response.result, "Salut")

    def test_translation_returns_invalid_response(self):
        response = self.provider.translate(TranslationRequest("", "eng"))
        self.assertFalse(response.status)
        self.assertIsNone(response.result)
