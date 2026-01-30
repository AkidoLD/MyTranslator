from translation.services import TranslateService
from translation.providers.exec_translation_api import ExecTranslationApi

provider = ExecTranslationApi(
    "TranslateService",
    "/home/akido-ld/.local/bin/trans",
    {"-b": ""},
    "_current:_target",
    10
)

translate = TranslateService(provider)

text = input("Veuillez entrer le texte que vous souhaitez traduire : ").strip()

trad = translate.trans(text, "en", "fr")

print(trad)
