import tkinter as tk
from tkinter import Frame, Button, Label
from tkinter.ttk import Combobox

from translation.ui.components.translation_entry import TranslationEntry
from translation.ui.components.translation_detail_widget import TranslationDetailWidget


class TranslationFrame(Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        #
        self.trans_frame = Frame(self)
        self.trans_bt = Button(self, text="Traduire", font=("Ubuntu", 20, "bold"))
        self.details_frame = Frame(self)
        #trans_frame content
        self.left_entry = TranslationEntry(self.trans_frame, bd= 1)
        self.right_entry = TranslationEntry(self.trans_frame,bd= 1)
        self.change_lang = Frame(self.trans_frame)
        #
        self.top_lang = Combobox(self.change_lang, width=8, font=("Ubuntu", 12, "bold"), state="readonly")
        self.central_text = Label(self.change_lang, text="To", font=("Ubuntu", 18, "bold"))
        self.bottom_lang = Combobox(self.change_lang, width=8, font=("Ubuntu", 12, "bold"), state="readonly")

        #Trans_info frame content
        self.details_title_frame = Frame(self.details_frame, bg="gray")
        self.details_content_frame = Frame(self.details_frame)
        self.details_title_lb = Label(self.details_title_frame, bg="gray", text="Details", font=("Ubuntu", 18, "bold"))
        self.details_count_lb = Label(self.details_title_frame, bg="gray", text="(0)", font=("Ubuntu", 18, "bold"))

        #Pack items of self
        self.trans_frame.pack(side="top", fill="x", pady=2, padx=2)
        self.trans_bt.pack(side="top", anchor="ne", pady=1, padx=2)
        self.details_frame.pack(side="top", fill="both", expand=True, pady=2, padx=2)

        #Pack items of trans_frame
        self.left_entry.grid(row=0, column=0, rowspan=1, columnspan=1, sticky="nsew")
        self.change_lang.grid(row=0, column=1, rowspan=1, columnspan=1, sticky="ns")
        self.right_entry.grid(row=0, column=2, rowspan=1, columnspan=1, sticky="nsew")
        #
        self.trans_frame.grid_columnconfigure(0, weight=1)
        self.trans_frame.grid_columnconfigure(1, weight=0)
        self.trans_frame.grid_columnconfigure(2, weight=1)

        #
        self.top_lang.pack(side="top", anchor="nw", expand=False, padx=(0, 8))
        self.central_text.pack(side="top", fill="y", expand=True)
        self.bottom_lang.pack(side="bottom", anchor="se", expand=False, padx=(8,0))

        #Pack items of details_frame
        self.details_title_frame.pack(side="top", fill="x", expand=False, pady=1)
        self.details_content_frame.pack(fill="both", expand=True, pady=1)
        self.details_title_lb.pack(side="left", padx=4)
        self.details_count_lb.pack(side="left", padx= 5)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x500")
    root.title("Exemple TraductionStack")

    frame = TranslationFrame(root)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    root.mainloop()
