import os
import tkinter as tk
from tkinter import Frame
from tkinter.ttk import Button, Style

from history.ui.history_frame import HistoryFrame
from shared.infra.utils.image_utils import ImageUtils
from shared.ui.components.menu_stack import MenuStack
from shared.ui.components.stack_frame import StackFrame
from translation.ui.translation_frame import TranslationFrame


class CentralBar(tk.Frame):
    _CONFIG_IMG_PATH = os.path.join(os.path.dirname(__file__), "../resources/icons8-config-100 (1).png")
    _TRANS_IMG_PATH = os.path.join(os.path.dirname(__file__), "../resources/icons8-translation-100.png")
    _HISTORY_IMG_PATH = os.path.join(os.path.dirname(__file__), "../resources/icons8-history-100 (2).png")
    #

    def __init__(self, parent):
        super().__init__(parent)
        #
        _size = 27
        self._config_img = ImageUtils.get_tk_image(self._CONFIG_IMG_PATH, _size)
        self._history_img = ImageUtils.get_tk_image(self._HISTORY_IMG_PATH, _size)
        self._trans_img = ImageUtils.get_tk_image(self._TRANS_IMG_PATH, _size)
        #
        self.nav_bar = Frame(self, height=35, relief="sunken", border=1, padx=2, background="#dadada")
        self.stack = StackFrame(self)
        #
        self.nav_bar.pack(side="top", fill="x")
        self.stack.pack(side="top", fill="both", expand=True)

        # Create stacks
        self.translation_frame : TranslationFrame = self.stack.add_item('trad', TranslationFrame)
        self.historic_frame : HistoryFrame = self.stack.add_item('hist', HistoryFrame)
        self.setting_frame : MenuStack = self.stack.add_item('setting', MenuStack)
        #
        buttons = [
            ("Traduction", "trad", self._trans_img),
            ("Historique", "hist", self._history_img),
            ("Paramètres", "setting", self._config_img),
        ]

        for text, tag, img in buttons :
            btn = Button(
                self.nav_bar,
                text=text,
                image=img,
                cursor="hand2",
                compound='left',
                style="Btn.CentralBar.TButton",
                padding=(4, 1)
            )
            #
            btn.pack(padx=2 , pady=2, side="left")
            btn.config(command=lambda t=tag : self.stack.raise_item(t))
        #
        Style().configure(
            "Btn.CentralBar.TButton",
            font=("Arial", 15),
            background="#f3f3f3",
            space=5
        )

    def on_switch_bt_clicked(self, tag):
        self.stack.raise_item(tag)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x500")
    central = CentralBar(root)
    central.pack(fill="both", expand=True)
    root.mainloop()
