import tkinter as tk
from tkinter.ttk import Style

from app.ui.bottom_bar import BottomBar
from app.ui.central_bar import CentralBar
from app.ui.top_bar import TopBar


class MainWindow(tk.Tk):

    def __init__(self):
        super().__init__()
        #
        self.title("MyTranslator")
        self.geometry("580x820")
        self.minsize(470, 450)
        #
        self._top_bar = TopBar(self, "MyTranslator")
        self._central_bar = CentralBar(self)
        self._bottom_bar = BottomBar(self)
        self._bottom_bar.config(height=50)
        #
        self._top_bar.pack(fill="x", side="top",)
        self._central_bar.pack(side="top", fill="both", expand=True)
        self._bottom_bar.pack(fill="x", side="bottom", expand=False)

    @property
    def app_name_lb(self):
        return self._top_bar.app_name_label

    @property
    def provider_combobox(self):
        return self._top_bar.provider_selector

    @property
    def translation_frame(self):
        return self._central_bar.translation_frame

    @property
    def history_frame(self):
        return self._central_bar.historic_frame

    @property
    def setting_frame(self):
        return self._central_bar.setting_frame


if __name__ == "__main__":
    root = MainWindow()
    root.mainloop()
