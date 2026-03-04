import tkinter as tk
from tkinter import Frame
from tkinter.ttk import Button

from history.ui.history_frame import HistoryFrame
from settings.ui.setting_frame import SettingFrame
from shared.ui.components.menu_stack import MenuStack
from shared.ui.components.stack_frame import StackFrame
from translation.ui.translation_frame import TranslationFrame


class CentralBar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.nav_bar = Frame(self, height=35, relief="sunken", border=1)
        self.stack = StackFrame(self)
        #
        self.nav_bar.pack(side="top", fill="x")
        self.stack.pack(side="top", fill="both", expand=True)

        # Create stacks
        self.translation_frame = self.stack.add_item('trad', TranslationFrame)
        self.historic_frame = self.stack.add_item('hist', HistoryFrame)
        self.setting_frame = self.stack.add_item('setting', MenuStack)
        #
        buttons = {
            "Traduire": "trad",
            "Historique": "hist",
            "Paramètres": "setting"
        }

        for text, tag in buttons.items():
            btn = Button(self.nav_bar, text=text, cursor="hand2")
            btn.pack(padx=1 , pady=1, side="left")
            btn.bind("<Button-1>", lambda e, t = tag: self.on_switch_bt_clicked(tag=t, event=e))

    def on_switch_bt_clicked(self, tag, event):
        self.stack.raise_item(tag)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x500")
    central = CentralBar(root)
    central.pack(fill="both", expand=True)
    root.mainloop()
