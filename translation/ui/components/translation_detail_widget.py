import tkinter as tk

from tkinter import Frame, Label

from PIL.ImageEnhance import Color

from shared.ui.components.clipboard_button import ClipboardButton


class TranslationDetailWidget(Frame):
    def __init__(self, master, title, value, **kwargs):
        super().__init__(master, **kwargs)
        #
        self.config(padx=2, pady=1, relief="solid", bd=1)
        self._title_lb = Label(self, text=title, bg=self["bg"], font=("Ubuntu", 14, "bold"))
        self._value_lb = Label(self, text=value, font=("Ubuntu", 14), bg=self["bg"])
        self._copy_btn = ClipboardButton(self, value, 25, bg=self["bg"], relief="flat")
        #
        self._title_lb.pack(side="left")
        self._value_lb.pack(side="left", expand=True, anchor="e", padx=10)
        self._copy_btn.pack(padx=2, pady=2)

if __name__ == "__main__" :
    root = tk.Tk()
    root.geometry("500x500")
    root.title("Test InfoWidget")
    f = Frame(root)
    f.pack(fill="both", expand=True)
    info = TranslationDetailWidget(f, "Synonyme", "Bonjour", bg="lightgray")
    info.pack(side="top", expand=True, fill="x")
    #
    root.mainloop()
