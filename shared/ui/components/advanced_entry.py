import tkinter as tk
from tkinter import StringVar

from tkinter.ttk import Entry, Button

from shared.infra.utils.validation_utils import validate_type


class AdvancedEntry(Entry):
    #Custom event
    TEXT_CHANGED = "<<TextChanged>>"

    def __init__(
            self,
            parent,
            text: str = "",
            textvariable : StringVar = None,
            placeholder: str = "",
            foreground: str = 'black',
            placeholder_color: str = "gray",
            **kwargs
    ):
        super().__init__(parent, **kwargs)
        #
        self.textvariable = textvariable or StringVar(self)
        self._placeholder = placeholder
        self._foreground = foreground
        self._placeholder_color = placeholder_color
        self._placeholder_is_shown = False
        #
        self.bind("<Control-v>", self._on_control_v)
        self.bind("<Control-a>", self._on_control_a)
        self.text = text


    def _on_control_a(self, _):
        if self._placeholder_is_shown: return "break"
        self.selection_range(0, 'end')
        return "break"

    def _on_control_v(self, _):
        self.text = self.text + self.clipboard_get()
        return "break"


    @property
    def textvariable(self) -> StringVar:
        return self._textvariable

    @textvariable.setter
    def textvariable(self, value : StringVar):
        self._textvariable : StringVar = validate_type(value, StringVar, "textvariable")
        self.configure(textvariable=value)
        self._textvariable.trace_add('write', self._on_text_changed)

    def _on_text_changed(self, *_):
        self._toggle_placeholder()
        self.event_generate(self.TEXT_CHANGED)

    @property
    def text(self):
        return "" if self._placeholder_is_shown else self.textvariable.get()

    @text.setter
    def text(self, value):
        self._hide_placeholder()
        self.textvariable.set(validate_type(value, str, "text"))

    @property
    def placeholder(self):
        return self._placeholder

    @placeholder.setter
    def placeholder(self, value):
        self._placeholder = validate_type(value, str, "placeholder")
        if self._placeholder_is_shown : self._show_placeholder(True)

    def get(self):
        return self.text

    def set(self, value : str):
        self.text = value

    def _toggle_placeholder(self):
        self._show_placeholder() if not self._placeholder_is_shown and not self.text else self._hide_placeholder()

    def _show_placeholder(self, force : bool = False):
        if not force and self._placeholder_is_shown: return
        #
        self.text = self._placeholder
        self.configure(foreground=self._placeholder_color)
        self._placeholder_is_shown = True
        #
        self._cursor_lock_id = self.bind("<ButtonPress>", self._lock_cursor, add="+")
        self.bind("<B1-Motion>", self._lock_cursor, add="+")
        self.bind("<Key>", self._lock_cursor, add="+")
        self.bind("<FocusIn>", self._lock_cursor, add="+")


    def _hide_placeholder(self):
        if not self._placeholder_is_shown: return
        #
        self.delete(1, 'end')
        self.configure(foreground=self._foreground)
        self._placeholder_is_shown = False
        #
        self.unbind("<ButtonPress>")
        self.unbind("<B1-Motion>")
        self.unbind("<Key>")
        self.unbind("<FocusIn>")
        #
        self.after(0, lambda _: super(AdvancedEntry, self).icursor('end'), None)

    def _lock_cursor(self, _):
        self.after(0, lambda _: super(AdvancedEntry, self).icursor(0), None)

if __name__ == "__main__" :
    root = tk.Tk()
    entry = AdvancedEntry(root, placeholder="Entrez votre texte ici...")
    entry.pack(padx=10, pady=10)
    Button(root, text="Focus moi").pack()
    root.mainloop()
