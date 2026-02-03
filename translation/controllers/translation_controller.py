import tkinter as tk
from tkinter import Event

from shared.ui.components.advanced_entry import AdvancedEntry
from translation.infra.persistance.json_translation_api_repository import JsonTranslationApiRepository
from translation.services.translation_service import TranslationService
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
        if not isinstance(trans_service, TranslationService):
            raise ValueError("The translation_service is not instance of TranslationService")
        #
        self._trans_service = trans_service
        self._trans_frame = trans_frame

        # Expose current widget
        self._focused_entry = self._trans_frame.left_entry
        self._unfocused_entry = self._trans_frame.right_entry
        #
        self._top_combobox = self._trans_frame.top_lang
        self._bottom_combobox = self._trans_frame.bottom_lang
        #
        self._focused_entry.combobox = self._top_combobox
        self._unfocused_entry.combobox = self._bottom_combobox
        #
        self._translate_btn = self._trans_frame.trans_bt
        #
        self._details_count_lb = self._trans_frame.details_count_lb
        self._details_frame = self._trans_frame.details_content_frame
        #
        self._initialize()

    def _initialize(self):
        self._focused_entry.bind(TranslationEntry.SMART_FOCUS_IN, self._on_translation_entry_focused)
        self._unfocused_entry.bind(TranslationEntry.SMART_FOCUS_IN, self._on_translation_entry_focused)
        self._translate_btn.bind("<Button-1>", self._on_translate_btn_clicked)
        #
        self._set_trans_entry_style()
        self.load_langages()
        #
        self._focused_entry.entry.bind(AdvancedEntry.EVENT_TEXT_CHANGED, lambda _ : self._check_trans_input())
        self._unfocused_entry.entry.bind(AdvancedEntry.EVENT_TEXT_CHANGED, lambda _ : self._check_trans_input())
        self._top_combobox.bind("<<ComboboxSelected>>",  lambda _ : self._check_trans_input())
        self._bottom_combobox.bind("<<ComboboxSelected>>", lambda _ : self._check_trans_input())
        self._check_trans_input()

    def load_langages(self):
        p = self._trans_service.active_provider
        if not p :
            raise RuntimeError("Failed to load langages. No translation api selected. Please, select one and retry")
        #
        langages = p.langages
        self._focused_entry.combobox["values"] = tuple(langages.keys())
        self._unfocused_entry.combobox["values"] = tuple(langages.keys())

    def _check_trans_input(self):
        is_valid = True
        if not self._focused_entry.text : is_valid = False
        if not self._unfocused_entry.combobox.get() : is_valid = False
        if not self._focused_entry.combobox.get() : is_valid = False
        #
        if not is_valid :
            self._translate_btn.config(state="disabled")
        else:
            self._translate_btn.config(state="active")

    def _on_translation_entry_focused(self, event : Event):
        if not event or not isinstance(event, Event) :
            raise TypeError("The type of event must be type of tkinter.Event. The actual is " + str(type(event)))
        #
        self._set_focused_entry(event.widget)
        self._check_trans_input()

    def _set_focused_entry(self, entry : TranslationEntry) -> None:
        """Set the focused_entry"""
        if not isinstance(entry, TranslationEntry) :
            raise TypeError("The entry must be type of TranslationEntry. Actual it is " + str(type(entry)))
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
            raise TypeError("Details must be type of dict")
        #Set the number of details
        nbr_details = len(details)
        self._details_count_lb.config(text="(" + str(nbr_details) + ")")

        #Clear the details Frame
        for child in self._details_frame.winfo_children():
            child.destroy()
        #
        for title, value in details.items() :
            detail_widget = TranslationDetailWidget(self._details_frame, title, value, bg="white")
            detail_widget.pack(side="top", anchor="n", fill="x", expand=False, padx=2, pady=2)

    def _on_translate_btn_clicked(self, _ : Event):
        text : str = self._focused_entry.text
        if not text.strip(): return

        #
        trans_provider = self._trans_service.active_provider
        #Retrieve langage
        src_lang = trans_provider.langages.get(self._focused_entry.combobox.get()) or ""
        dest_lang = trans_provider.langages.get(self._unfocused_entry.combobox.get()) or ""
        #
        try:
            result = self._trans_service.translate(text, dest_lang, src_lang)
            self._unfocused_entry.text = result.translated
            #show details
            self._display_translation_details(result.details)
        except RuntimeError as e :
            print("Oups, une erreur est survenu or de la traduction : ", e)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x400")

    # name = "Trans"
    # binary = "/home/akido-ld/.local/bin/trans"
    # args = {"-b": ""}
    # lang_template = "_current:_target"
    # #
    # provider = ExecTranslationApi(None, name, binary, args, lang_template, {"francais" : "fr", "Anglais" : "en", "Espagnol" : "es"}, True)

    repo = JsonTranslationApiRepository("api_list.json")
    providers = repo.load()
    #
    service = TranslationService(providers)
    #
    print(providers)
    #
    view = TranslationFrame(root)
    view.place(relwidth=1, relheight=1)
    #
    controller = TranslationController(view, service)

    root.mainloop()

