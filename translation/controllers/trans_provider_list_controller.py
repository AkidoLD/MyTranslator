import tkinter
from typing import List
from tkinter import messagebox


from translation.domain.models.translation_provider import TranslationProvider
from translation.infra.persistance.json_translation_provider_repository import JsonTranslationProviderRepository
from translation.services.translation_service import TranslationService
from translation.ui.components.trans_provider_data import TransProviderData
from translation.ui.setting.provider_list_frame import ProviderListFrame


class TranslationProviderListController:
    def __init__(self, trans_provider_list_frame : ProviderListFrame, translation_service : TranslationService):
        if not isinstance(translation_service, TranslationService):
            raise TypeError(f"trans_service must be TranslationService, got type {type(trans_provider_list_frame).__name__}")
        #
        if not isinstance(trans_provider_list_frame, ProviderListFrame):
            raise TypeError(
                f"trans_provider_list_frame must be ProviderListFrame, got type {type(trans_provider_list_frame).__name__}"
            )
        #
        self._trans_service = translation_service
        self._trans_provider_list_frame = trans_provider_list_frame
        #
        self._trans_provider_list_frame.on_search = self._on_search
        self._trans_provider_list_frame._on_refresh_btn_clicked = self._on_refresh_btn_clicked
        self._trans_provider_list_frame.on_provider_deleted = self._on_delete_btn_clicked
        #
        self._display_all_provider()

    def _display_providers(self, providers : List[TranslationProvider]):
        providers = [TransProviderData(
            provider.id,
            provider.name,
            provider.type,
            len(provider.languages),
            provider.req_internet,
        ) for provider in providers]
        #
        self._trans_provider_list_frame.set_providers(providers)

    def _display_all_provider(self):
        self._display_providers(self._trans_service.providers)

    def _on_refresh_btn_clicked(self):
        self._trans_provider_list_frame.clear_search_bar()
        self._display_all_provider()

    def _on_delete_btn_clicked(self, provider_id):
        provider =  self._trans_service.get_provider(provider_id)
        if not provider : return
        #
        if not messagebox.askyesno("Titre", f"Êtes-vous sûr de vouloir supprimer le fournisseur {provider.name} ?") : return
        #
        self._trans_service.remove_provider(provider_id)
        self._trans_provider_list_frame.remove_provider(provider_id)

    def _on_search(self, value : str):
        if not isinstance(value, str) : return
        #
        providers = [provider for provider in self._trans_service.providers if value.lower() in provider.name.lower()]
        self._display_providers(providers)


if __name__ == "__main__":
    root = tkinter.Tk()
    root.geometry("500x500")
    root.title("ProviderListFrame Test")

    frame = ProviderListFrame(
        root,
        on_refresh_btn_clicked=lambda: print("Refresh clicked"),
        on_search=lambda q: print(f"Recherche : {q}"),
        on_provider_clicked=lambda pid: print(f"Provider clicked : {pid}"),
        on_provider_deleted=lambda pid: print(f"Provider deleted : {pid}"),
    )

    #
    provider_repo = JsonTranslationProviderRepository("../../tmp_api_config.json")
    trans_service = TranslationService(provider_repo)
    #
    control = TranslationProviderListController(frame, trans_service)
    #
    frame.pack(fill="both", expand=True)

    root.mainloop()