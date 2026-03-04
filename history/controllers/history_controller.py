import math
import tkinter
from tkinter import Event, StringVar
from tkinter.ttk import Combobox
from typing import List


from history.infra.providers.fake_history_repository import FakeHistoryRepository
from history.services.history_service import HistoryService
from history.ui.history_frame import HistoryFrame
from shared.infra.events.event_bus import event_bus
from shared.infra.events.events import HistoryEvents
from translation.infra.integration.history.translation_history_entry import TranslationHistoryEntry
from translation.infra.integration.history.translation_history_provider import TranslationHistoryProvider


class HistoryController:
    def __init__(self, history_frame : HistoryFrame, history_service : HistoryService):
        if not isinstance(history_frame, HistoryFrame) :
            raise TypeError(f"The history_frame must be type of HistoryFrame. The actual is {type(history_frame)}")
        #
        if not isinstance(history_service, HistoryService) :
            raise TypeError(f"The history_service must be type of HistoryService. The actual is {type(history_service)}")
        #
        #
        self._history_frame = history_frame
        self._history_service = history_service
        #
        self._histories_pane = self._history_frame.content_pane
        self._history_selector = history_frame.history_selector
        self._first_page_bt = history_frame.first_page_btn
        self._previous_page_bt = history_frame.previous_page_btn
        self._page_selection_spin = history_frame.page_selection_spin
        self._page_count_lb = history_frame.page_count_lb
        self._next_page_bt = history_frame.next_page_btn
        self._last_page_bt = history_frame.last_page_btn
        #
        self._displayed_spin = history_frame.displayed_spin
        self._refresh_btn = history_frame.refresh_btn
        self._displayable_lb = history_frame.displayable_lb
        #
        self._displayed_page_var = StringVar()
        self._page_count_var = StringVar()
        self._displayed_count_var = StringVar()
        self._displayable_count_var = StringVar()
        #
        self.initialize()

    def initialize(self):
        self._init_title_pane()
        self._init_config_pane()
        #
        self.load_provider_selector_values()
        #
        self._history_selector.bind("<<ComboboxSelected>>", self._on_provider_selected)
        #
        event_bus.subscribe(HistoryEvents.ENTRY_ADDED, lambda _ : self.load_active_provider_history())

    def _init_title_pane(self):
        self._history_selector.config(justify="center")
        self._history_selector.set("-- select --")
        self.load_provider_selector_values()


    def _init_config_pane(self):
        self._page_selection_spin.config(from_=1, to=1, justify="right", textvariable=self._displayed_page_var)
        self._displayed_spin.config(from_=0, to= 999, justify="right", textvariable=self._displayed_count_var)
        self._page_count_lb.config(textvariable=self._page_count_var)
        self._displayable_lb.config(textvariable=self._displayable_count_var)
        #
        self._displayed_page_var.set("1")
        self._page_count_var.set("1")
        #
        self._displayed_count_var.set("10")
        self._displayable_count_var.set("0")

        #Binding
        self._first_page_bt.bind("<Button-1>", self._on_first_bt_clicked)
        self._previous_page_bt.bind("<Button-1>", self._on_previous_bt_clicked)
        self._next_page_bt.bind("<Button-1>", self._on_next_bt_clicked)
        self._last_page_bt.bind("<Button-1>", self._on_last_bt_clicked)
        self._refresh_btn.bind("<Button-1>", self._on_refresh_btn_clicked)
        #
        self._page_selection_spin.bind("<Return>", self._on_displayed_page_enter)
        self._displayed_spin.bind("<Return>", self._on_displayable_enter)
        #
        self._page_selection_spin.bind("<KP_Enter>", self._on_displayed_page_enter)
        self._displayed_spin.bind("<KP_Enter>", self._on_displayable_enter)

    def _update_config_pane(self):
        provider = self._history_service.active_provider
        if not provider  :
            print("No history provider set")
            return
        #
        history_count = self._history_service.get_provider_history_count(provider)
        displayed_count = int(self._displayed_count_var.get() or 10)
        #
        page_count = max(math.ceil(history_count / (displayed_count or 1)) , 1)
        displayed_page = min(int(self._displayed_page_var.get()), page_count)
        #
        self._page_count_var.set(str(page_count))
        self._displayed_page_var.set(str(displayed_page))
        #
        self._displayed_count_var.set(str(displayed_count))
        self._displayable_count_var.set(str(history_count))
        #
        self._page_selection_spin.config(to=page_count)

    def load_provider_selector_values(self):
        self._history_selector.config(values=[provider.title for provider in self._history_service.providers])

    def _get_provider_values_map(self) -> dict:
        return {provider.title: provider.provider_key for provider in self._history_service.providers}

    def load_active_provider_history(self):
        provider = self._history_service.active_provider
        if not provider :
            print("No provider set.")
            return
        #
        self._update_config_pane()
        #
        _offset = int(self._displayed_count_var.get()) * (int(self._displayed_page_var.get()) - 1)
        _limit  = int(self._displayed_count_var.get())

        self._history_frame.clear_content_frame()
        #
        try :
            entries = self._history_service.get_provider_history(provider, _offset, _limit)
            widgets = [provider.create_entry_widget(self._histories_pane, entry) for entry in entries]
            #
            for w in widgets : w.pack(side="top", expand=True, fill="x", pady=4, padx= 2)
            #
        except (RuntimeError, TypeError, ValueError) as e:
            print(f"Failed to load history of {provider.title}", e)

    def _on_provider_selected(self, event : Event):
        if not isinstance(event.widget, Combobox) : return
        widget : Combobox = event.widget
        #
        value = widget.get()
        if not value :
            print("No provider selected")
            return
        #
        key = self._get_provider_values_map().get(widget.get())
        if not key :
            print(f"The provider with the name {widget.get()} is not found")
            return
        #
        try : self._history_service.set_active_provider(key)
        except ValueError as e :
            print(f"Failed to set the active provider with key {key}", e)
            return
        #
        self.load_active_provider_history()

    # >>>>>>>>>>>>>>>>> BUTTONS ACTIONS <<<<<<<<<<<<<<<<<<<<<<#
    def _on_first_bt_clicked(self, _ : Event):
        self._displayed_page_var.set("1")
        self.load_active_provider_history()

    def _on_previous_bt_clicked(self, _ : Event):
        new_value = max(int(self._displayed_page_var.get()) - 1, 1)
        self._displayed_page_var.set(str(new_value))
        #
        self.load_active_provider_history()

    def _on_next_bt_clicked(self, _ : Event):
        new_value = min(int(self._displayed_page_var.get()) + 1, int(self._page_count_var.get()))
        self._displayed_page_var.set(str(new_value))
        #
        self.load_active_provider_history()

    def _on_last_bt_clicked(self, _ : Event):
        new_value = int(self._page_count_var.get())
        self._displayed_page_var.set(str(new_value))
        #
        self.load_active_provider_history()

    def _on_refresh_btn_clicked(self, _ : Event):
        self._update_config_pane()
        self.load_active_provider_history()

    # >>>>>>>>>>>>>>>>> SPINS ACTIONS <<<<<<<<<<<<<<<<<<<<<<#
    def _on_displayed_page_enter(self, _ : Event):
        self.load_active_provider_history()

    def _on_displayable_enter(self, _ : Event):
        self.load_active_provider_history()




if __name__ == "__main__":
    root = tkinter.Tk()
    root.geometry("500x400")

    repo = FakeHistoryRepository()
    fake_trans_hist : List[TranslationHistoryEntry]= [
        TranslationHistoryEntry(None, f"Traduction {i}", f"Translation {i}", "fr", "en", None) for i in range(1, 20)]
    #
    t_provider = TranslationHistoryProvider()
    service = HistoryService(repo, [t_provider])
    #
    for p in fake_trans_hist : service.add_history_entry(p)
    #
    view = HistoryFrame(root)
    view.place(relwidth=1, relheight=1)
    #
    controller = HistoryController(view, service)

    root.mainloop()
