import tkinter

from shared.infra.utils.validation_utils import validate_type
from translation.controllers.setting.add_provider_controller import AddProviderController
from translation.controllers.setting.provider_list_controller import ProviderListController
from translation.controllers.setting.update_provider_controller import UpdateProviderController
from translation.infra.persistance.json_translation_provider_repository import JsonTranslationProviderRepository
from translation.application.services.translation_service import TranslationService
from translation.ui.translation_setting_frame import TranslationSettingFrame


class TranslationSettingController:
    def __init__(self, translation_setting_frame : TranslationSettingFrame, translation_service : TranslationService):
        self._translation_setting_frame : TranslationSettingFrame = validate_type(
            translation_setting_frame, TranslationSettingFrame, "translation_setting_frame")
        #
        self._translation_service : TranslationService = validate_type(
            translation_service, TranslationService, "translation_service")
        #
        self._provider_list_frame = self._translation_setting_frame.provider_list_frame
        self._add_provider_frame = self._translation_setting_frame.add_provider_frame
        self._update_provider_frame = self._translation_setting_frame.update_provider_frame
        #
        self._add_provider_controller = AddProviderController(translation_service, self._add_provider_frame)
        self._update_provider_controller = UpdateProviderController(translation_service, self._update_provider_frame)
        self._provider_list_controller = ProviderListController(translation_service, self._provider_list_frame)
        #
        self._add_provider_frame.on_back_btn_clicked = self._on_back_btn_clicked
        self._update_provider_frame.on_back_btn_clicked = self._on_back_btn_clicked
        #
        self._provider_list_frame.on_provider_clicked = self._on_provider_clicked
        self._provider_list_frame.on_add_btn_clicked = self._on_add_btn_clicked

    def _on_provider_clicked(self, provider_id):
        provider = self._translation_service.get_provider(provider_id)
        if not provider :
            self._translation_setting_frame.error_dialog(
                "Échec de recuperation du fournisseur",
                f"Aucun fournisseur avec l'ID {provider_id} n'a ete trouve."
            )
            return
        #
        self._update_provider_controller.display_provider_data(provider)
        self._translation_setting_frame.show_update_provider_frame()
        #

    def _on_add_btn_clicked(self):
        self._add_provider_controller.reset_fields()
        self._translation_setting_frame.show_add_provider_frame()

    def _on_back_btn_clicked(self):
        self._provider_list_controller.refresh_content()
        self._translation_setting_frame.show_provider_list_frame()

if __name__ == "__main__" :
    root = tkinter.Tk()
    root.geometry("500x400")
    #
    repo = JsonTranslationProviderRepository("../../tmp_api_config.json")
    service = TranslationService(repo)
    view = TranslationSettingFrame(root)
    control = TranslationSettingController(view, service)

    view.pack(fill='both', expand=True)
    #
    root.mainloop()