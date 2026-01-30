import tkinter as tk
from tkinter import Label, Frame

class BottomBar(Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.config(bg="white")

        self.app_name = Label(self, text="MyTranslator", font=("Ubuntu", 12, "bold"), bg=self["bg"], fg="#333")
        self.by_text = Label(self, text="by", font=("Ubuntu", 10), bg=self["bg"], fg="#555")
        self.author = Label(self, text="AkidoLD", font=("Ubuntu", 12, "italic"), bg=self["bg"], fg="#222")
        self.year = Label(self, text="@2025", font=("Ubuntu", 10), bg=self["bg"], fg="#555")

        self.year.pack(side="right", padx=(5,0))
        self.author.pack(side="right", padx=(5,0))
        self.by_text.pack(side="right", padx=(5,0))
        self.app_name.pack(side="right", padx=(5,0))


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x50")
    bottom = BottomBar(root)
    bottom.pack(side="bottom", fill="x")
    root.mainloop()
