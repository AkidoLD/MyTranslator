import tkinter
import uuid

from shared.infra.utils.validation_utils import validate_type
from translation.infra.factories.translation_provider_form_factory import TranslationProviderFormFactory
from translation.infra.persistance.json_translation_provider_repository import JsonTranslationProviderRepository
from translation.application.services.translation_service import TranslationService
from translation.ui.components.provider_basic_data_form import ProviderBasicDataForm
from translation.ui.components.provider_data_form import ProviderDataForm
from translation.ui.setting.add_provider_frame import AddProviderFrame


class AddProviderController:
    _DEFAULT_LANGUAGES = {
        "Francais" : "fr",
        "Anglais" : "en",
        "Espagnol" : "es",
        "Japonais": "ja"
    }
    #
    _DEFAULT_TIMEOUT = 5

    def __init__(self,  translation_service : TranslationService, add_provider_frame : AddProviderFrame):
        self._translation_service : TranslationService = validate_type(
            translation_service, TranslationService, "translation_service")
        self._add_provider_frame : AddProviderFrame = validate_type(
            add_provider_frame, AddProviderFrame, "add_provider_frame")
        #
        add_provider_frame.advanced_data_forms = TranslationProviderFormFactory.get_advanced_forms()
        self.reset_fields()
        #
        self._add_provider_frame.on_add_btn_clicked = self._on_add_btn_clicked
        self._add_provider_frame.on_reset_btn_clicked = self._on_reset_btn_clicked

    def _on_reset_btn_clicked(self):
        self._add_provider_frame.provider_data_form.reset()
        self.reset_fields()

    def _on_add_btn_clicked(self):
        data = self._add_provider_frame.get_form_data()
        #
        try :
            provider = TranslationProviderFormFactory.create_from_form_data(data)
        except (RuntimeError, ValueError) as e :
            self._add_provider_frame.error_dialog("Failed add provider",
                                                  f"An error occurred during provider adding : {str(e)}")
            return
        #
        if not self._add_provider_frame.confirm_dialog("Confirmer l'ajouter d'un fournisseur",
                                                       f"Etes-vous sure de vouloir ajouter le fournisseur {provider.name} ?"): return
        #
        self._translation_service.add_provider(provider)
        #
        self.reset_fields()

    def reset_fields(self):
        self._add_provider_frame.provider_data_form.reset()
        #
        self._add_provider_frame.set_form_data({ProviderDataForm.BASIC_DATA_FORM : {
            ProviderBasicDataForm.PROVIDER_ID_FIELD : str(uuid.uuid4()),
            ProviderBasicDataForm.PROVIDER_REQ_INTERNET_FIELD : True,
            ProviderBasicDataForm.PROVIDER_DETECT_SRC_LANG_FIELD: False,
            ProviderBasicDataForm.PROVIDER_LANGUAGES_FIELD : self._DEFAULT_LANGUAGES,
            ProviderBasicDataForm.PROVIDER_TIMEOUT_FIELD :self._DEFAULT_TIMEOUT
        }})
        #

if __name__ == "__main__" :
    root = tkinter.Tk()
    root.geometry("500x400")
    #
    service = TranslationService(JsonTranslationProviderRepository("../../../tmp_api_config.json"))
    view = AddProviderFrame(root)
    controller = AddProviderController(service, view)

    view.pack(fill='both', expand=True)
    #
    root.mainloop()