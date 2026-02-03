import tkinter as tk
from tkinter import Frame, StringVar

from shared.ui.components.clipboard_button import ClipboardButton
from shared.ui.components.advanced_entry import AdvancedEntry
from shared.ui.components.float_menu import FloatFrame
from shared.ui.mixins.smart_events import SmartEventMixin


class TranslationEntry(SmartEventMixin, Frame):
    def __init__(self, parent, placeholder: str | None = None, **kwargs):
        super().__init__(parent, **kwargs)
        self.config(bg="gray")
        #
        self._var_text = StringVar
        self._entry = AdvancedEntry(self, placeholder=placeholder, placeholder_color="light gray", bg=self['bg'], relief="flat", highlightthickness="0")
        self._entry.config(font=("Ubuntu", 20))
        #
        self.float_menu = FloatFrame(self, True)
        self.clipboard_bt = ClipboardButton(self.float_menu, self._entry.get_text, relief="raised")
        self.clipboard_bt.pack()
        #
        self._entry.pack(side="top", pady=60, padx=30, anchor="center", fill="x", expand=True)

        #
        self.bind(self.SMART_ENTER, self._on_enter_entry)
        self.bind(self.SMART_LEAVE, self._on_leave_entry)
        self.bind(self.SMART_L_CLICK, lambda  e : self._entry.focus_set())
        #


    def _get_entry_text(self):
        return self._entry.text

    def _on_enter_entry(self, _ = None):
        x, y = self.winfo_rootx() + 5, self.winfo_rooty() + 5
        self.float_menu.move_to(x, y)
        self.float_menu.show()

    def _on_leave_entry(self, _ = None):
        self.float_menu.hide()

    @property
    def entry(self):
        return self._entry

    @property
    def text(self):
        return self._entry.text

    @text.setter
    def text(self, value : str):
        self._entry.text = value

    @property
    def placeholder(self):
        return self._entry.placeholder

    @placeholder.setter
    def placeholder(self, value : str):
        self._entry.placeholder = value

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x200")

    entry = TranslationEntry(root, placeholder="Entrez le texte ici ...")
    entry.pack(fill="x", pady=10, padx=10)

    root.mainloop()
