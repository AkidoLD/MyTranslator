from typing import Dict, Type, Any

from translation.domain.models.translation_provider import TranslationProvider
from translation.infra.enums.translation_provider_type import TranslationProviderType
from translation.infra.providers.translation.exec_translation_provider import ExecTranslationProvider
from translation.infra.providers.translation.fake_translation_provider import FakeTranslationProvider
from translation.infra.providers.translation.http_translation_provider import HttpTranslationProvider
from translation.infra.providers.translation.lib_translation_provider import LibTranslationProvider


class TranslationProviderFactory:

    _providers: Dict[TranslationProviderType, Type[TranslationProvider]] = {
        TranslationProviderType.EXEC: ExecTranslationProvider,
        TranslationProviderType.HTTP: HttpTranslationProvider,
        TranslationProviderType.LIB: LibTranslationProvider,
        TranslationProviderType.FAKE: FakeTranslationProvider,
    }

    @classmethod
    def create_from_dict(cls, data: dict) -> TranslationProvider:
        provider_type = data.get("type")
        if not provider_type:
            raise ValueError("Missing 'type' field in provider data")

        provider_class = cls._providers.get(provider_type)
        if not provider_class:
            raise ValueError(f"Unknown provider _type: {provider_type}")

        return provider_class.from_dict(data)