from abc import abstractmethod, ABC


class DialogService(ABC):
    @abstractmethod
    def confirm_dialog(self, title: str, message: str) -> bool: pass

    @abstractmethod
    def info_dialog(self, title: str, message: str): pass

    @abstractmethod
    def error_dialog(self, title: str, message: str): pass

    @abstractmethod
    def warning_dialog(self, title: str, message: str): pass