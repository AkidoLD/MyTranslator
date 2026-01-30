import os.path
import tkinter as tk
from tkinter import Button, Entry, StringVar

from PIL import Image, ImageTk


class ClipboardButton(Button):
    def __init__(self, parent, getter, size : int = 25, **kwargs):
        super().__init__(parent, **kwargs)
        #
        self.getter = getter
        self.bind("<Button-1>", self.on_bt_clicked)

        #Get the clipboard image
        path = f"{os.path.dirname(__file__)}/../../resources/icons8-copy-96.png"
        self.size = size
        self.img = ImageTk.PhotoImage(Image.open(path).resize((self.size, self.size)))
        self.config(image=self.img, cursor="hand2")


    def on_bt_clicked(self, event):
        if callable(self.getter):
            value = self.getter()
        else:
            value = self.getter
        #If the value is empty, do nothing
        if not value:
            return
        self.clipboard_clear()
        self.clipboard_append(value)
        print(f"Clipboard [new] : {value}")

if __name__ == "__main__" :
    root = tk.Tk()
    root. geometry("400x400")
    text = StringVar(root)
    entry = Entry(root, textvariable=text)
    entry.pack()
    clip = ClipboardButton(root, entry.get, 40)
    clip.pack()
    root.mainloop()
