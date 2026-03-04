import tkinter

from app.controllers.app_controller import AppController
from app.services.app_service import AppService
from app.ui.about_frame import AboutFrame
from app.ui.main_window import MainWindow
from history.controllers.history_controller import HistoryController
from history.infra.providers.fake_history_repository import FakeHistoryRepository
from history.services.history_service import HistoryService
from shared.ui.components.menu_stack import MenuStack
from translation.controllers.trans_provider_list_controller import TranslationProviderListController
from translation.controllers.translation_controller import TranslationController
from translation.infra.integration.history.translation_history_provider import TranslationHistoryProvider
from translation.infra.persistance.json_translation_provider_repository import JsonTranslationProviderRepository
from translation.services.translation_service import TranslationService
from translation.ui.setting.provider_list_frame import ProviderListFrame


class Application:

    def __init__(self):
        self._main_window = MainWindow()

        #Translation Module
        self._trans_repository = JsonTranslationProviderRepository("api_config.json")
        self._trans_service = TranslationService(self._trans_repository)
        self._trans_controller = TranslationController(self._main_window.translation_frame, self._trans_service)
        self._trans_history_provider = TranslationHistoryProvider()

        #History Module
        self._history_repository = FakeHistoryRepository()
        self._history_service = HistoryService(self._history_repository, [self._trans_history_provider])
        self._history_controller = HistoryController(self._main_window.history_frame, self._history_service)

        #Setting
        self._setting_view : MenuStack = self._main_window.setting_frame
        #
        app_view = self._setting_view.add_menu("app_setting", "Application", tkinter.Frame, bg="white")
        #
        info_view = self._setting_view.add_menu("app_about", "A propos", AboutFrame, group_id="app_setting", app_version="1.0.0", app_creator="AkidoLD")
        #
        self._trans_setting_view = self._setting_view.add_menu("translation", "Traduction", ProviderListFrame)
        self._translation_provider_list_controller = TranslationProviderListController(self._trans_setting_view, self._trans_service)


        #Application Module
        self._app_service = AppService(self._trans_service, self._history_service)
        self._app_controller = AppController(self._main_window, self._app_service)
        #

    def run(self):
        self._main_window.mainloop()
