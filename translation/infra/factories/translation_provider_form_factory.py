from typing import Dict, Callable, Any, Type

from translation.domain.models.translation_provider import TranslationProvider
from translation.infra.enums.translation_provider_type import TranslationProviderType
from translation.application.factories.translation_provider_factory import TranslationProviderFactory
from translation.infra.providers.translation.exec_translation_provider import ExecTranslationProvider
from translation.infra.providers.translation.fake_translation_provider import FakeTranslationProvider
from translation.ui.components.provider_advanced_forms.exec_provider_advanced_data_form import ExecProviderAdvancedDataForm, ProviderAdvancedDataForm
from translation.ui.components.provider_advanced_forms.fake_provider_advanced_data_form import \
    FakeProviderAdvancedDataForm
from translation.ui.components.provider_basic_data_form import ProviderBasicDataForm
from translation.ui.components.provider_data_form import ProviderDataForm


class TranslationProviderFormFactory:

    @staticmethod
    def get_advanced_forms() -> Dict[str, Type[ProviderAdvancedDataForm]]:
        return {
            TranslationProviderType.EXEC: ExecProviderAdvancedDataForm,
            TranslationProviderType.FAKE: FakeProviderAdvancedDataForm
        }

    # --- Parsers : form data -> provider ---

    @classmethod
    def _get_advanced_parsers(cls) -> Dict[str, Callable[[dict], dict]]:
        return {
            TranslationProviderType.EXEC: cls._parse_exec_data,
            TranslationProviderType.FAKE: cls._parse_fake_data,
        }

    @staticmethod
    def _parse_exec_data(data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            ExecTranslationProvider.KEY_BINARY: data.get(ExecProviderAdvancedDataForm.PROVIDER_BINARY_FIELD),
            ExecTranslationProvider.KEY_LANG_TEMPLATE: data.get(ExecProviderAdvancedDataForm.PROVIDER_LANG_TEMPLATE_FIELD),
            ExecTranslationProvider.KEY_ARGS: data.get(ExecProviderAdvancedDataForm.PROVIDER_ARGS_FIELD),
        }

    @staticmethod
    def _parse_fake_data(data: Dict[str, Any]) -> Dict[str, Any]: return {}

    # --- Serializers : provider -> form data ---

    @classmethod
    def _get_advanced_serializers(cls) -> dict:
        return {
            TranslationProviderType.EXEC : cls._serialize_exec_data,
            TranslationProviderType.FAKE : cls._serialize_fake_data
        }

    @staticmethod
    def _serialize_exec_data(provider: ExecTranslationProvider) -> dict:
        return {
            ExecProviderAdvancedDataForm.PROVIDER_BINARY_FIELD: provider.binary,
            ExecProviderAdvancedDataForm.PROVIDER_LANG_TEMPLATE_FIELD: provider.lang_template,
            ExecProviderAdvancedDataForm.PROVIDER_ARGS_FIELD: provider.arguments,
        }

    @staticmethod
    def _serialize_fake_data(provider : FakeTranslationProvider): return {}

    # --- Public API ---

    @classmethod
    def create_from_form_data(cls, data: Dict[str, dict]) -> TranslationProvider:
        _basic_data: dict = data.get(ProviderDataForm.BASIC_DATA_FORM)
        _advanced_data: dict = data.get(ProviderDataForm.ADVANCED_DATA_FORM)
        _type = _basic_data.get(ProviderBasicDataForm.PROVIDER_TYPE_FIELD)
        if not _type:
            raise RuntimeError("Failed to retrieve provider data from form. No provider type found.")

        parser: Callable[[dict], dict] = cls._get_advanced_parsers().get(_type)
        if not parser:
            raise RuntimeError(f"No parser found for provider type: {_type}")

        provider_data = {
            TranslationProvider.KEY_ID: _basic_data.get(ProviderBasicDataForm.PROVIDER_ID_FIELD),
            TranslationProvider.KEY_NAME: _basic_data.get(ProviderBasicDataForm.PROVIDER_NAME_FIELD),
            TranslationProvider.KEY_TYPE: _type,
            TranslationProvider.KEY_TIMEOUT: float(_basic_data.get(ProviderBasicDataForm.PROVIDER_TIMEOUT_FIELD)),
            TranslationProvider.KEY_REQ_INTERNET: _basic_data.get(ProviderBasicDataForm.PROVIDER_REQ_INTERNET_FIELD),
            TranslationProvider.KEY_DETECT_SRC_LANG: _basic_data.get(ProviderBasicDataForm.PROVIDER_DETECT_SRC_LANG_FIELD),
            TranslationProvider.KEY_LANGUAGES: _basic_data.get(ProviderBasicDataForm.PROVIDER_LANGUAGES_FIELD),
            **parser(_advanced_data)
        }

        return TranslationProviderFactory.create_from_dict(provider_data)

    @classmethod
    def to_form_data(cls, provider: TranslationProvider) -> Dict[str, dict]:
        serializer = cls._get_advanced_serializers().get(provider.get_type())
        if not serializer:
            raise RuntimeError(f"No serializer found for provider type: {provider.get_type()}")

        basic_data = {
            ProviderBasicDataForm.PROVIDER_ID_FIELD: provider.id,
            ProviderBasicDataForm.PROVIDER_NAME_FIELD: provider.name,
            ProviderBasicDataForm.PROVIDER_TYPE_FIELD: provider.get_type(),
            ProviderBasicDataForm.PROVIDER_TIMEOUT_FIELD: str(provider.timeout),
            ProviderBasicDataForm.PROVIDER_REQ_INTERNET_FIELD: provider.req_internet,
            ProviderBasicDataForm.PROVIDER_DETECT_SRC_LANG_FIELD: provider.detect_src_lang,
            ProviderBasicDataForm.PROVIDER_LANGUAGES_FIELD: provider.languages,
        }

        return {
            ProviderDataForm.BASIC_DATA_FORM: basic_data,
            ProviderDataForm.ADVANCED_DATA_FORM: serializer(provider),
        }