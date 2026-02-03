import os.path
import tkinter as tk
from tkinter import Button, StringVar, Entry, Event
from typing import Callable

from PIL import Image, ImageTk
from PIL.Image import Resampling


class ClipboardButton(Button):
    def __init__(self, parent, value_getter : str | Callable[[], str], size: int = 25, **kwargs):
        #
        super().__init__(parent, **kwargs)
        self.value_getter = value_getter
        #image path
        self._path = os.path.join(os.path.dirname(__file__),"../../resources/icons8-copy-96.png")
        self._source_image = Image.open(self._path)
        self._size = size
        self._update_image()
        #
        self.config(cursor="hand2")
        self.bind("<Button-1>", self._on_clicked)

    def _update_image(self):
        resized = self._source_image.resize((self._size, self._size), Resampling.LANCZOS)
        self._img = ImageTk.PhotoImage(resized)
        self.config(image=self._img)

    def _on_clicked(self,_ : Event):
        value = self._value_getter if isinstance(self._value_getter, str) else self._value_getter()
        if not value : return
        #
        self.clipboard_clear()
        self.clipboard_append(value)
        self.update()

    @property
    def size(self) -> int:
        return self._size

    @size.setter
    def size(self, value: int):
        if value <= 0:
            raise ValueError("The size must be greater than 0")
        #
        self._size = value
        self._update_image()

    @property
    def value_getter(self):
        return self._value_getter

    @value_getter.setter
    def value_getter(self, value : str | Callable[[], str]):
        if not (callable(value) or isinstance(value, str)):
            raise TypeError("value_getter must be a callable or a string")
        #
        self._value_getter = value


if __name__ == "__main__" :
    root = tk.Tk()
    root. geometry("400x400")
    text = StringVar(root)
    entry = Entry(root, textvariable=text)
    entry.pack()
    clip = ClipboardButton(root, text.get)
    clip.pack()
    root.mainloop()
