import tkinter as tk

from tkinter import Entry, Event, Button, StringVar


class AdvancedEntry(Entry):
    #Custom event
    EVENT_TEXT_CHANGED = "<<TextChanged>>"

    def __init__(
            self,
            parent,
            text: str = "",
            placeholder: str = "",
            text_color: str | None = None,
            placeholder_color: str | None = None,
            **kwargs
    ):
        super().__init__(parent, **kwargs)

        self._var_text = StringVar(value=text)
        self.config(textvariable=self._var_text)
        self._placeholder = placeholder
        self._text_color = text_color if text_color else "black"
        self._placeholder_color = placeholder_color if placeholder_color else "gray"
        self._placeholder_is_shown = False
        #Show the placeholder if it's needed
        self._show_placeholder() if self._var_text.get() == "" else self._hide_placeholder()
        #
        self.bind("<FocusIn>", self._on_focus_in)
        self.bind("<FocusOut>", self._on_focus_out)
        self._var_text.trace_add("write", self._on_text_changed)

    def _on_text_changed(self, *_):
        self.event_generate(self.EVENT_TEXT_CHANGED)

    def _on_focus_in(self, event):
        if self._placeholder_is_shown:
            self._hide_placeholder()

    def _on_focus_out(self, event):
        if not self.get():  # Si vide
            self._show_placeholder()

    def _show_placeholder(self):
        if self._placeholder_is_shown:
            return
        #
        self._var_text.set(self._placeholder or "")
        self.config(fg=self._placeholder_color)
        self._placeholder_is_shown = True

    def _hide_placeholder(self):
        if not self._placeholder_is_shown:
            return
        #
        self._var_text.set("")
        self.config(fg=self._text_color)
        self._placeholder_is_shown = False


    def set_text(self, value : str):
        if value == "":
            return
        #
        self._hide_placeholder()
        self._var_text.set(value)

    def get_text(self):
        return "" if self._placeholder_is_shown else self._var_text.get()

    def set_placeholder(self, value : str):
        self._placeholder = value
        if self._placeholder_is_shown:
            self.var_text.set(value)

    def get_placeholder(self):
        return self._placeholder

    @property
    def placeholder(self):
        return self.get_placeholder()

    @placeholder.setter
    def placeholder(self, value : str):
        self.set_placeholder(value)

    @property
    def text(self):
        return self.get_text()

    @text.setter
    def text(self, value : str):
        self.set_text(value)

    @property
    def var_text(self):
        return self._var_text

    @var_text.setter
    def var_text(self, value : StringVar):
        if not isinstance(value, StringVar) :
            raise TypeError("The var_text must be StringVar type.")
        #
        self._var_text = value

if __name__ == "__main__" :
    root = tk.Tk()
    entry = AdvancedEntry(root, placeholder="Entrez votre texte ici...")
    entry.pack(padx=10, pady=10)
    Button(root, text="Focus moi").pack()
    root.mainloop()
