import tkinter
from typing import Dict, Any

from shared.infra.utils.validation_utils import validate_type
from translation.domain.models.translation_provider import TranslationProvider
from translation.infra.factories.translation_provider_form_factory import TranslationProviderFormFactory
from translation.application.services.translation_service import TranslationService
from translation.infra.persistance.json_translation_provider_repository import JsonTranslationProviderRepository
from translation.ui.setting.update_provider_frame import UpdateProviderFrame


class UpdateProviderController:
    def __init__(self, translation_service: TranslationService, update_provider_frame : UpdateProviderFrame):
        self._translation_service: TranslationService = validate_type(
            translation_service, TranslationService, "translation_service")
        #
        self._update_provider_frame: UpdateProviderFrame = validate_type(
            update_provider_frame, UpdateProviderFrame, "update_provider_frame")
        #
        self.provider_data_snapshot : Dict[str, Any] = {}
        #
        update_provider_frame.advanced_data_forms = TranslationProviderFormFactory.get_advanced_forms()
        #
        update_provider_frame.on_save_btn_clicked = self._on_save_btn_clicked

    def display_provider_data(self, provider : TranslationProvider):
        self.provider_data_snapshot = provider.to_dict()
        #
        self._update_provider_frame.set_form_data(TranslationProviderFormFactory.to_form_data(provider))
        self._update_provider_frame.readonly = True

    @property
    def provider_data_snapshot(self) -> dict:
        return self._provider_data_snapshot
    
    @provider_data_snapshot.setter
    def provider_data_snapshot(self, value : dict):
        self._provider_data_snapshot = validate_type(value, dict, "provider_data_snapshot")

    def _on_save_btn_clicked(self):
        _data = self._update_provider_frame.provider_data_form.get()
        #
        try :
            provider = TranslationProviderFormFactory.create_from_form_data(_data)
        except (RuntimeError, ValueError) as e:
            self._update_provider_frame.error_dialog("Failed update provider data",
                                                     f"An error occurred during provider adding : {str(e)}")
            return
        #
        _provider_data = provider.to_dict()
        _changes = {k : v for k, v in _provider_data.items() if v != self.provider_data_snapshot.get(k)}
        #
        if not _changes : return
        #
        self._translation_service.update_provider(_provider_data.get(TranslationProvider.KEY_ID), _changes)
        self._update_provider_frame.info_dialog(
            "Changement applique",
            f"Mise a jour du fournisseur {_provider_data.get(TranslationProvider.KEY_NAME)} reussite.\nListe de changements : \n" +
            f"{"".join(f"- {k} : {self.provider_data_snapshot.get(k, "--")} -> {v}\n" for k, v in _changes.items())}"
        )
        #
        self.provider_data_snapshot = _provider_data

if __name__ == "__main__" :
    root = tkinter.Tk()
    root.geometry("500x400")
    #
    service = TranslationService(JsonTranslationProviderRepository("../../../tmp_api_config.json"))
    view = UpdateProviderFrame(root)
    controller = UpdateProviderController(service, view)
    view.pack(fill='both', expand=True)
    #
    root.mainloop()