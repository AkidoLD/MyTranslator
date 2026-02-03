from typing import Dict, Type

from translation.domain.base.translation_api import TranslationApi
from translation.infra.enums import TranslationApiType
from translation.infra.providers.exec_translation_api import ExecTranslationApi
from translation.infra.providers.http_translation_api import HttpTranslationApi
from translation.infra.providers.lib_translation_api import LibTranslationApi

API_PROVIDER_MAP : Dict[TranslationApiType, Type[TranslationApi]]= {
    TranslationApiType.EXEC : ExecTranslationApi,
    TranslationApiType.HTTP : HttpTranslationApi,
    TranslationApiType.LIB : LibTranslationApi,
}

def get_translation_provider(api_type : TranslationApiType):
    cls = API_PROVIDER_MAP.get(api_type)
    if cls is None :
        raise ValueError(f"Api type {api_type} is not implemented")
    return cls