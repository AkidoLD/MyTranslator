import tkinter as tk
from tkinter import Frame
from tkinter.ttk import Style

from shared.infra.utils.validation_utils import validate_type
from shared.ui.components.clipboard_button import ClipboardButton
from shared.ui.components.advanced_entry import AdvancedEntry
from shared.ui.components.float_menu import FloatFrame
from shared.ui.mixins.smart_events import SmartEventMixin


class TranslationEntry(SmartEventMixin, Frame):
    _STYLE_ENTRY = "Entry.TranslationEntry.TEntry"
    _DEFAULT_BG = "gray"

    def __init__(self, parent, placeholder: str = "", background: str = _DEFAULT_BG, **kwargs):
        super().__init__(parent, **kwargs)
        self.config(bg=background)
        #
        self._configure_styles(background)
        self._build_ui(placeholder)
        self._bind_events()

    def _configure_styles(self, background: str):
        Style().configure(
            self._STYLE_ENTRY,
            relief="flat",
            background=background,
            fieldbackground=background,
            borderwidth=0,
            lightcolor=background,
            darkcolor=background,
        )

        Style().layout(
            self._STYLE_ENTRY,[
                ("Entry.padding", {"sticky": "nswe", "children": [
                    ("Entry.textarea", {"sticky": "nswe"})
                ]})
            ]
        )

    def _build_ui(self, placeholder: str | None):
        self._entry = AdvancedEntry(
            self,
            placeholder=placeholder,
            placeholder_color="light gray",
            style=self._STYLE_ENTRY
        )
        self._entry.config(font=("Ubuntu", 20))
        self._entry.pack(side="top", pady=60, padx=30, anchor="center", fill="x", expand=True)
        #
        self._float_menu = FloatFrame(self, True)
        self._clipboard_btn = ClipboardButton(self._float_menu, self._entry.get, relief="raised")
        self._clipboard_btn.pack()

    def _bind_events(self):
        self.bind(self.SMART_ENTER, self._on_enter_entry)
        self.bind(self.SMART_LEAVE, self._on_leave_entry)
        self.bind(self.SMART_L_CLICK, lambda _: self._entry.focus_set())

    def _on_enter_entry(self, _=None):
        x = self.winfo_rootx() + self.winfo_width() - (self._float_menu.winfo_reqwidth() + 5)
        y = self.winfo_rooty() + 5
        self._float_menu.move_to(x, y)
        self._float_menu.show()

    def _on_leave_entry(self, _=None):
        self._float_menu.hide()

    # ─── Properties ───────────────────────────────────────────────────────────

    @property
    def entry(self) -> AdvancedEntry:
        return self._entry

    @property
    def text(self) -> str:
        return self._entry.text

    @text.setter
    def text(self, value: str):
        validate_type(value, str, "text")
        self._entry.text = value

    @property
    def placeholder(self) -> str:
        return self._entry.placeholder

    @placeholder.setter
    def placeholder(self, value: str):
        validate_type(value, str, "placeholder")
        self._entry.placeholder = value


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x200")

    TranslationEntry(root, placeholder="Entrez le texte ici ...", background="gray").pack(fill="x", pady=10, padx=10)

    root.mainloop()