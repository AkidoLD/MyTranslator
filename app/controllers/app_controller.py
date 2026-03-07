
from app.services.app_service import AppService
from app.ui.main_window import MainWindow
from shared.infra.events.event_bus import event_bus
from translation.application.services.translation_service import TranslationService
from translation.domain.models.translation_provider import TranslationProvider
from translation.infra.integration.history.translation_history_entry import TranslationHistoryEntry
from translation.ui.components.provider_combobox import ProviderCombobox


class AppController:
    def __init__(self, main_window : MainWindow, app_service : AppService):
        self._main_window = main_window
        self._app_service = app_service
        #
        self._trans_frame = main_window.translation_frame
        self._provider_combobox = main_window.provider_combobox
        #
        self.load_provider_combobox_providers()
        self._provider_combobox.bind(ProviderCombobox.PROVIDER_SELECTED, self._on_provider_combobox_selected)
        #
        event_bus.subscribe(TranslationService.TRANS_COMPLETED, self._on_translation_completed)
        event_bus.subscribe(TranslationService.TRANS_PROVIDER_ADDED, self._on_trans_providers_changed)
        event_bus.subscribe(TranslationService.TRANS_PROVIDER_REMOVED, self._on_trans_providers_changed)
        event_bus.subscribe(TranslationService.TRANS_PROVIDER_UPDATE, self._on_trans_providers_changed)

    def _on_translation_completed(self, data : dict):
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

    def _on_trans_providers_changed(self, _ : dict):
        self.load_provider_combobox_providers()

    def load_provider_combobox_providers(self):
        self._provider_combobox.values = ((items.id, items.name, items.req_internet) for items in self._app_service.get_app_providers())
        selected : TranslationProvider = self._app_service.get_active_provider()

        #Display the selected provider
        data = (selected.id, selected.name, selected.req_internet) if selected else None
        self._provider_combobox.set(data)

    def _on_provider_combobox_selected(self, _):
        self._app_service.set_active_provider(self._provider_combobox.get()[0])
