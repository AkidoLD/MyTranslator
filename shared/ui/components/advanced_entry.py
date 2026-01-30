import tkinter as tk

from tkinter import Entry, Event, Button


class AdvancedEntry(Entry):
    def __init__(
            self,
            parent,
            text : str | None = None,
            placeholder: str | None = None,
            text_color : str | None = None,
            placeholder_color : str | None = None,
            **kwargs
    ):
        super().__init__(parent, **kwargs)
        #
        if text :
            self.insert(0, text)
        self._text_color = text_color or "black"
        #
        self._placeholder = placeholder
        self._placeholder_color = placeholder_color or "gray"
        #
        self.placeholder_display = True if not self.get() else False
        self._show_placeholder()
        # Bind focus in/out
        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out)

    def set_text_color(self, color : str):
        self._text_color = color

    def get_text_color(self):
        return self._text_color

    def set_placeholder_color(self, color : str):
        self._placeholder_color = color

    def get_placeholder_color(self):
        return self._placeholder_color

    def _show_placeholder(self):
        if self._placeholder and not self.get():
            self.insert(0, self._placeholder)
            self.config(fg=self._placeholder_color)
            self.placeholder_display = True

    def _hide_placeholder(self):
        if self.placeholder_display:
            self.delete(0, tk.END)
            self.config(fg=self._text_color)
            self.placeholder_display = False

    def on_focus_in(self, event: Event):
        self._hide_placeholder()

    def on_focus_out(self, event: Event):
        self._show_placeholder()

if __name__ == "__main__" :
    root = tk.Tk()
    entry = AdvancedEntry(root, placeholder="Entrez votre texte ici...")
    entry.pack(padx=10, pady=10)
    Button(root, text="Focus moi").pack()
    root.mainloop()
