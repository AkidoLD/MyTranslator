from tkinter import Event

from app.services.app_service import AppService
from app.ui.main_window import MainWindow
from shared.infra.events.event_bus import event_bus
from shared.infra.events.events import Events
from translation.domain.models.translation_result import TranslationResult
from translation.infra.integration.history.translation_history_entry import TranslationHistoryEntry
from translation.ui.components.api_combobox import ApiComboBox


class AppController:
    def __init__(self, main_window : MainWindow, app_service : AppService):
        self._main_window = main_window
        self._app_service = app_service
        #
        self._trans_frame = main_window.translation_frame
        self._api_combobox = main_window.api_combobox
        #
        self.load_api_combobox_providers()
        self._api_combobox.bind(ApiComboBox.API_SELECTED, self._on_api_combobox_selected)
        #
        event_bus.subscribe(Events.TRANSLATION_COMPLETED, self._on_translation_completed)

    def _on_translation_completed(self, result : TranslationResult):
        if not isinstance(result, TranslationResult) :
            raise TypeError("The result must by type of TranslationResult")
        #
        history_entry = TranslationHistoryEntry(None, result.original, result.translated, result.src_lang, result.target_lang, None)
        self._app_service.append_history_entry(history_entry)

    def load_api_combobox_providers(self):
        self._api_combobox.values = ((items.id, items.name, items.required_internet) for items in self._app_service.get_app_providers())
        selected = self._app_service.get_active_provider()

        #Display the selected provider
        if selected and hasattr(selected, "id"):
            self._api_combobox.set_selected_api(selected.id)

    def _on_api_combobox_selected(self, event : Event):
        widget : ApiComboBox = event.widget
        if not isinstance(widget, ApiComboBox):
            raise TypeError("")
        #
        provider_id = widget.get()
        self._app_service.set_active_provider(provider_id)
