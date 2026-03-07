from history.domain.interfaces.history_entry_data import HistoryEntryData
from history.application.services.history_service import HistoryService
from translation.application.services.translation_service import TranslationService


class AppService:

    def __init__(self, trans_service : TranslationService, history_service : HistoryService):
        if not isinstance(trans_service, TranslationService) :
            raise TypeError("The trans_service must be _type of TranslationService.")
        #
        if not isinstance(history_service, HistoryService):
            raise TypeError("The history_service must be _type of HistoryService")
        #
        self._trans_service = trans_service
        self._history_service = history_service

    def get_active_provider(self):
        return self._trans_service.active_provider

    def set_active_provider(self, provider_id):
        self._trans_service.active_provider = provider_id

    def get_app_providers(self):
        return self._trans_service.providers

    def append_history_entry(self, history_entry : HistoryEntryData):
        if not isinstance(history_entry, HistoryEntryData):
            raise TypeError("The history_entry must be _type of HistoryEntryData")
        #
        self._history_service.add_history_entry(history_entry)