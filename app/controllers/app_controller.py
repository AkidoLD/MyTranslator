from app.ui.main_window import MainWindow
from translation.controllers.translation_controller import TranslationController
from translation.infra.persistance.json_translation_api_repository import JsonTranslationApiRepository
from translation.services.translation_service import TranslationService
from translation.ui.components.api_combobox import ApiComboBox


class AppController:
    def __init__(self, main_window : MainWindow):
        self._main_window = main_window
        self._translation_frame = main_window.central_bar.translation_frame
        self._api_selector = main_window.top_bar.api_selector
        #
        self._translation_repo = JsonTranslationApiRepository("translation_api.json")
        repo = self._translation_repo.load()
        self._translation_service = TranslationService(repo)
        self._api_selector.values = ((items.id, items.name, items.required_internet) for items in repo)
        self._translation_controller = TranslationController(self._translation_frame, self._translation_service)
        #
        self._api_selector.bind(ApiComboBox.API_SELECTED, lambda e : self._translation_service.set_active_provider(self._api_selector.get()))