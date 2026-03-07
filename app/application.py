from tkinter import Frame

from app.controllers.app_controller import AppController
from app.services.app_service import AppService
from app.ui.about_frame import AboutFrame
from app.ui.main_window import MainWindow
from history.controllers.history_controller import HistoryController
from history.infra.providers.fake_history_repository import FakeHistoryRepository
from history.application.services.history_service import HistoryService
from translation.controllers.translation_controller import TranslationController
from translation.controllers.translation_setting_controller import TranslationSettingController
from translation.infra.integration.history.translation_history_provider import TranslationHistoryProvider
from translation.application.services.translation_service import TranslationService
from translation.infra.persistance.json_translation_provider_repository import JsonTranslationProviderRepository
from translation.ui.translation_setting_frame import TranslationSettingFrame


class Application:

    def __init__(self):
        #Init repositories
        self.trans_provider_repo = JsonTranslationProviderRepository("t_provider_repo.json")
        self.history_repo = FakeHistoryRepository()

        #Init services
        self.trans_service = TranslationService(self.trans_provider_repo)
        self.history_service = HistoryService(self.history_repo, [TranslationHistoryProvider()])
        self.app_service = AppService(self.trans_service, self.history_service)

        #Init views
        self.main_window = MainWindow()
        self.trans_frame = self.main_window.translation_frame
        self.history_frame = self.main_window.history_frame
        self.setting_frame = self.main_window.setting_frame
        #
        self.app_setting_frame = self.setting_frame.add_menu(
            "Application",
            Frame,
            "app_setting",
            bg="white"
        )
        #
        self.about_frame = self.setting_frame.add_menu(
            "A Propos",
            AboutFrame,
            group_id="app_setting",
            app_creator="AkidoLD",
            app_version="1.0.0"
        )
        #
        self.trans_setting_frame = self.setting_frame.add_menu(
            "Traduction",
            TranslationSettingFrame
        )

        #Init controllers
        self.app_controller = AppController(self.main_window, self.app_service)
        self.trans_controller = TranslationController(self.trans_frame, self.trans_service)
        self.history_controller = HistoryController(self.history_frame, self.history_service)
        #
        self.trans_setting_controller = TranslationSettingController(self.trans_setting_frame, self.trans_service)
        #



    def run(self):
        self.main_window.mainloop()
