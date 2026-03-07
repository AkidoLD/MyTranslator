import tkinter as tk
from tkinter.ttk import Style

from shared.ui.components.clipboard_button import ClipboardButton
from shared.ui.components.advanced_entry import AdvancedEntry
from shared.ui.mixins.smart_events import SmartEventMixin


class TranslationEntry(SmartEventMixin, AdvancedEntry):
    _STYLE = "TranslationEntry.TEntry"

    def __init__(self, parent, placeholder: str = "", background: str = "gray", **kwargs):
        super().__init__(
            parent,
            placeholder=placeholder,
            placeholder_color="light gray",
            style=self._STYLE,
            **kwargs
        )
        self.config(font=("Ubuntu", 20))
        #
        self._background = background
        #
        self._setup_styles()
        self._build_ui()
        self._bind_events()

    # ─── Setup ────────────────────────────────────────────────────────────────

    def _setup_styles(self):
        Style().configure(
            self._STYLE,
            background=self._background,
            fieldbackground=self._background,
            lightcolor=self._background,
            darkcolor=self._background,
            borderwidth=0,
            focuscolor="black",
            padding=(30, 50)
        )
        Style().configure(self._STYLE, focuscolor="black")
        Style().map(self._STYLE, focuscolor=[("focus", "black")])

    def _build_ui(self):
        self._clipboard_btn = ClipboardButton(
            self.winfo_toplevel(),
            self.get,
            relief="flat",
            takefocus=0
        )
        self._clipboard_btn.master = self

    def _bind_events(self):
        self.bind(self.SMART_ENTER, lambda _: self._show_clipboard())
        self.bind(self.SMART_LEAVE, lambda _: self._hide_clipboard())

    # ─── Handlers ─────────────────────────────────────────────────────────────

    def _show_clipboard(self):
        self._clipboard_btn.place(in_=self, x=self.winfo_width() - 5, y=5, anchor="ne")
        self._clipboard_btn.lift()

    def _hide_clipboard(self):
        self._clipboard_btn.place_forget()


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x200")
    print(Style().layout('TEntry'))
    print(Style().element_options('TEntry.field'))
    TranslationEntry(root, placeholder="Entrez le texte ici ...", background="gray").pack(fill="x", pady=10, padx=10)
    root.mainloop()