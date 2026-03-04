from tkinter import Event

from app.services.app_service import AppService
from app.ui.main_window import MainWindow
from shared.infra.events.event_bus import event_bus
from shared.infra.events.events import TranslationEvents
from translation.infra.integration.history.translation_history_entry import TranslationHistoryEntry
from translation.ui.components.provider_combobox import ProviderComboBox


class AppController:
    def __init__(self, main_window : MainWindow, app_service : AppService):
        self._main_window = main_window
        self._app_service = app_service
        #
        self._trans_frame = main_window.translation_frame
        self._provider_combobox = main_window.provider_combobox
        #
        self.load_provider_combobox_providers()
        self._provider_combobox.bind(ProviderComboBox.PROVIDER_SELECTED, self._on_api_combobox_selected)
        #
        event_bus.subscribe(TranslationEvents.COMPLETED, self._on_translation_completed)

    def _on_translation_completed(self, data : dict):
        if not isinstance(data, dict) :
            raise TypeError(f"Result must by type of dict, got {type(data).__name__}")
        #
        history_entry = TranslationHistoryEntry(
            None,
            data.get("original", ""),
            data.get("translated", ""),
            data.get("src_lang", ""),
            data.get("target_lang", ""),
            None
        )
        #
        self._app_service.append_history_entry(history_entry)

    def load_provider_combobox_providers(self):
        self._provider_combobox.values = ((items.id, items.name, items.req_internet) for items in self._app_service.get_app_providers())
        selected = self._app_service.get_active_provider()

        #Display the selected provider
        if selected and hasattr(selected, "id"):
            self._provider_combobox.set_selected_provider(selected.id)

    def _on_api_combobox_selected(self, event : Event):
        widget : ProviderComboBox = event.widget
        if not isinstance(widget, ProviderComboBox):
            raise TypeError("")
        #
        provider_id = widget.get()
        self._app_service.set_active_provider(provider_id)
