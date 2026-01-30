import tkinter as tk
from tkinter import Frame
from shared.ui.components.clipboard_button import ClipboardButton
from shared.ui.components.advanced_entry import AdvancedEntry
from shared.ui.components.float_menu import FloatFrame
from shared.ui.mixins.smart_events import SmartEventMixin


class TranslationEntry(SmartEventMixin, Frame):
    def __init__(self, parent, placeholder: str | None = None, **kwargs):
        super().__init__(parent, **kwargs)
        self.config(bg="gray")
        self.entry = AdvancedEntry(self, placeholder=placeholder, bg=self['bg'], placeholder_color="white", relief="flat", highlightthickness="0")
        self.entry.config(font=("Ubuntu",20))
        self.float_menu = FloatFrame(self, True)
        self.clipboard_bt = ClipboardButton(self.float_menu, self._get_entry_text, relief="flat")
        self.clipboard_bt.pack()
        #
        self.entry.pack(side="top", pady=60, padx=30, anchor="center", fill="x", expand=True)

        #
        self.bind(self.SMART_ENTER, self._on_enter_entry)
        self.bind(self.SMART_LEAVE, self._on_leave_entry)
        self.bind(self.SMART_L_CLICK, lambda  e : self.entry.focus_set())

    def _get_entry_text(self):
        if self.entry.placeholder_display:
            return ""
        return self.entry.get()


    def _on_enter_entry(self,event = None):
        x, y = self.winfo_rootx() + 5, self.winfo_rooty() + 5
        self.float_menu.move_to(x, y)
        self.float_menu.show()

    def _on_leave_entry(self, event = None):
        self.float_menu.hide()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x200")

    entry = TranslationEntry(root, placeholder="Entrez le texte ici ...")
    entry.pack(fill="x", pady=10, padx=10)

    root.mainloop()
