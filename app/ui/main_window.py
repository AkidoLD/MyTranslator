import tkinter as tk

from app.ui.bottom_bar import BottomBar
from app.ui.central_bar import CentralBar
from app.ui.top_bar import TopBar


class MainWindow(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("MyTranslator")
        self.geometry("580x820")
        self.minsize(500, 500)
        #
        self.top_bar = TopBar(self, "MyTranslator")
        self.central_bar = CentralBar(self)
        self.bottom_bar = BottomBar(self)
        self.bottom_bar.config(height=50)
        #
        self.top_bar.pack(fill="x", side="top",)
        self.central_bar.pack(side="top", fill="both", expand=True)
        self.bottom_bar.pack(fill="x", side="bottom", expand=False)


if __name__ == "__main__":
    root = MainWindow()
    root.mainloop()
