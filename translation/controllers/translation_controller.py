import tkinter as tk
from tkinter import Event

from shared.infra.events.event_bus import event_bus
from shared.ui.components.advanced_entry import AdvancedEntry
from translation.domain.exceptions.translation_error import TranslationTimeOutError, TranslationError, \
    ProviderUnavailableError, UnsupportedLanguageError
from translation.domain.models.translation_provider import TranslationProvider
from translation.infra.persistance.json_translation_provider_repository import JsonTranslationProviderRepository
from translation.application.services.translation_service import TranslationService
from translation.ui.components.translation_entry import TranslationEntry
from translation.ui.components.translation_detail_widget import TranslationDetailWidget
from translation.ui.translation_frame import TranslationFrame


class TranslationController:
    FOCUSED_ENTRY_PLACEHOLDER = "Traduction"
    UNFOCUSED_ENTRY_PLACEHOLDER = "Réponse"

    def __init__(self, trans_frame : TranslationFrame, trans_service : TranslationService):
        #Check Arguments
        if not isinstance(trans_frame, TranslationFrame) :
            raise ValueError("The translation_frame is not instance of TranslationFrame")
        #
        if not isinstance(trans_service, TranslationService):
            raise ValueError("The translation_service is not instance of TranslationService")
        #
        self._trans_service = trans_service
        self._trans_frame = trans_frame

        # Expose current widget
        self._focused_entry = self._trans_frame.left_entry
        self._unfocused_entry = self._trans_frame.right_entry
        #
        self._top_combobox = self._trans_frame.top_combobox
        self._bottom_combobox = self._trans_frame.bottom_combobox
        #
        self._focused_entry.combobox = self._top_combobox
        self._unfocused_entry.combobox = self._bottom_combobox
        #
        self._translate_btn = self._trans_frame.trans_btn
        #
        self._details_count_lb = self._trans_frame.details_count_lb
        self._details_frame = self._trans_frame.details_content_frame
        #
        self._initialize()

    def _initialize(self):
        self._init_translation_pane()
        #
        self._focused_entry.bind(TranslationEntry.SMART_FOCUS_IN, self._on_translation_entry_focused)
        self._unfocused_entry.bind(TranslationEntry.SMART_FOCUS_IN, self._on_translation_entry_focused)
        #
        self._translate_btn.config(command=self._on_translate_btn_clicked)
        #
        self._focused_entry.entry.bind(AdvancedEntry.TEXT_CHANGED, lambda _ : self._check_translation_fields())
        self._unfocused_entry.entry.bind(AdvancedEntry.TEXT_CHANGED, lambda _ : self._check_translation_fields())
        self._top_combobox.bind("<<ComboboxSelected>>", lambda _ : self._check_translation_fields())
        self._bottom_combobox.bind("<<ComboboxSelected>>", lambda _ : self._check_translation_fields())
        #
        self._focused_entry.entry.bind("<KP_Enter>", self._on_translation_entry_enter)
        self._unfocused_entry.entry.bind("<KP_Enter>", self._on_translation_entry_enter)
        self._focused_entry.entry.bind("<Return>", self._on_translation_entry_enter)
        self._unfocused_entry.entry.bind("<Return>", self._on_translation_entry_enter)
        #
        event_bus.subscribe(TranslationService.TRANS_PROVIDER_CHANGED, self._on_active_provider_changed)
        event_bus.subscribe(TranslationService.TRANS_PROVIDER_REMOVED, self._on_trans_provider_removed)
        event_bus.subscribe(TranslationService.TRANS_PROVIDER_UPDATE, self._on_trans_provider_update)

    def _init_translation_pane(self):
        self._top_combobox.config(justify="center")
        self._bottom_combobox.config(justify="center")
        #
        self._focused_entry.combobox.set("-- select --")
        self._unfocused_entry.combobox.set("-- select --")
        #
        self._set_trans_entry_style()
        self._load_langages()
        self._check_translation_fields()

    def _on_active_provider_changed(self, _ : dict):
        self._load_langages()
        self._check_translation_fields()

    def _on_trans_provider_update(self, data : dict):
        provider_id = data.get(TranslationProvider.KEY_ID)
        if not self._trans_service.active_provider or provider_id != self._trans_service.active_provider.id : return
        #
        self._load_langages()
        self._check_translation_fields()

    def _on_trans_provider_removed(self, _ : dict):
        self._load_langages()
        self._check_translation_fields()

    def _load_langages(self):
        provider = self._trans_service.active_provider
        if not provider : print("No provider set. Selection one before.")
        #
        values = tuple(provider.languages.keys()) if provider else ()
        #
        self._focused_entry.combobox["values"] = values
        self._unfocused_entry.combobox["values"] = values
        #
        if self._focused_entry.combobox.get() not in values :
            self._focused_entry.combobox.set("-- select --")
        #
        if self._unfocused_entry.combobox.get() not in values :
            self._unfocused_entry.combobox.set("-- select --")

    def _check_translation_fields(self):
        is_valid = True
        provider = self._trans_service.active_provider
        #
        if not provider :
            is_valid = False
        else :
            languages =  provider.languages
            detect_src = self._trans_service.active_provider.detect_src_lang
            #
            if not self._focused_entry.text : is_valid = False
            if not  detect_src and self._focused_entry.combobox.get() not in languages: is_valid = False
            if self._unfocused_entry.combobox.get() not in languages : is_valid = False
        #
        self._translate_btn.config(state="normal" if is_valid else "disabled")
        #
        return is_valid

    def _on_translation_entry_enter(self, _ : Event):
        self._perform_translation()

    def _on_translation_entry_focused(self, event : Event):
        if not isinstance(event, Event) :
            return
        #
        self._set_focused_entry(event.widget)
        self._check_translation_fields()

    def _set_focused_entry(self, entry : TranslationEntry) -> None:
        if not isinstance(entry, TranslationEntry) :
            return
        #
        if entry == self._focused_entry : return
        #
        self._focused_entry, self._unfocused_entry \
            = entry, self._focused_entry
        #Update the entry style
        self._set_trans_entry_style()

    def _set_trans_entry_style(self):
        self._focused_entry.config(bd=1, relief="solid")
        self._unfocused_entry.config(bd=1, relief="flat")
        #
        self._focused_entry.placeholder = self.FOCUSED_ENTRY_PLACEHOLDER
        self._unfocused_entry.placeholder = self.UNFOCUSED_ENTRY_PLACEHOLDER

    def _display_translation_details(self, details : dict):
        if not isinstance(details, dict) :
            return

        #Set the number of details
        self._details_count_lb.config(text="(" + str(len(details)) + ")")

        self._clear_details_pane()
        #
        for title, value in details.items() :
            detail_widget = TranslationDetailWidget(self._details_frame, title, value, bg="white")
            detail_widget.pack(side="top", anchor="n", fill="x", expand=False, padx=2, pady=2)

    def _clear_details_pane(self):
        for child in self._details_frame.winfo_children(): child.destroy()

    def _perform_translation(self):
        if not self._check_translation_fields() : return
        #
        text: str = self._focused_entry.text
        if not text.strip(): return
        #
        provider = self._trans_service.active_provider
        # Retrieve langage
        src_lang = provider.languages.get(self._focused_entry.combobox.get(), "")
        dest_lang = provider.languages.get(self._unfocused_entry.combobox.get(), "")
        #
        try:
            result = self._trans_service.translate(text, dest_lang, src_lang)
            self._unfocused_entry.text = result.translated
            # show details
            self._trans_frame.after(0, self._display_translation_details, result.details)
            #
            # self._display_translation_details(result.details)
        except (TranslationTimeOutError, ProviderUnavailableError, UnsupportedLanguageError, TranslationError) as e :
            self._trans_frame.after(
                0,
                self._trans_frame.error_dialog,
                "Échec de traduction",
                f"Une erreur est survenu lors de la tentative de traduction : \n{str(e)}"
            )

    def _on_translate_btn_clicked(self):
        self._trans_frame.after(0, self._perform_translation, )

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x400")
    #
    repo = JsonTranslationProviderRepository("../../tmp_api_config.json")
    #
    service = TranslationService(repo)
    #
    view = TranslationFrame(root)
    view.place(relwidth=1, relheight=1)
    #
    controller = TranslationController(view, service)

    root.mainloop()

