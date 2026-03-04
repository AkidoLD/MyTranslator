import os
import tkinter as tk
from tkinter import Frame, Button
from tkinter.ttk import Combobox, Label

from shared.infra.utils.image_utils import ImageUtils
from shared.ui.components.scroll_pane import ScrollPane
from translation.ui.components.translation_entry import TranslationEntry


class TranslationFrame(Frame):
    _TRANSLATION_BT_IMG_PATH = os.path.join(os.path.dirname(__file__), "../resources/icons8-translate-100.png")

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        #
        self._trans_bt_img = ImageUtils.convert_to_tk_image(
            ImageUtils.get_image(self._TRANSLATION_BT_IMG_PATH, (40, 40)))
        #
        self._trans_frame = Frame(self)
        self._trans_bt = Button(self, text="Traduire", image=self._trans_bt_img, compound="left", font=("Ubuntu", 20, "bold"), cursor="hand2")
        self._details_frame = Frame(self)
        #trans_frame content
        self._left_entry = TranslationEntry(self._trans_frame, border= 1)
        self._right_entry = TranslationEntry(self._trans_frame,border= 1)
        self._change_lang = Frame(self._trans_frame)
        #
        self._top_lang = Combobox(self._change_lang, width=10, font=("Ubuntu", 12, "bold"), state="readonly")
        self._central_text = Label(self._change_lang, text="To", font=("Ubuntu", 18, "bold"))
        self._bottom_lang = Combobox(self._change_lang, width=10, font=("Ubuntu", 12, "bold"), state="readonly")

        #Trans_info frame content
        self._details_content_scroll = ScrollPane(self._details_frame, background=self['bg'])
        self._details_title_frame = Frame(self._details_frame, bg="gray")
        self._details_content_frame = self._details_content_scroll.pane
        self._details_title_lb = Label(self._details_title_frame, background="gray", text="Details", font=("Ubuntu", 18, "bold"))
        self._details_count_lb = Label(self._details_title_frame, background="gray", text="(0)", font=("Ubuntu", 18, "bold"))

        #Pack items of self
        self._trans_frame.pack(side="top", fill="x", pady=2, padx=2)
        self._trans_bt.pack(side="top", anchor="ne", pady=1, padx=2)
        self._details_frame.pack(side="top", fill="both", expand=True, pady=2, padx=2)

        #Pack items of trans_frame
        self._left_entry.grid(row=0, column=0, rowspan=1, columnspan=1, sticky="nsew")
        self._change_lang.grid(row=0, column=1, rowspan=1, columnspan=1, sticky="ns")
        self._right_entry.grid(row=0, column=2, rowspan=1, columnspan=1, sticky="nsew")
        #
        self._trans_frame.grid_columnconfigure(0, weight=1)
        self._trans_frame.grid_columnconfigure(1, weight=0)
        self._trans_frame.grid_columnconfigure(2, weight=1)

        #
        self._top_lang.pack(side="top", anchor="nw", expand=False, padx=(0, 8))
        self._central_text.pack(side="top", fill="y", expand=True)
        self._bottom_lang.pack(side="bottom", anchor="se", expand=False, padx=(8,0))

        #Pack items of details_frame
        self._details_title_frame.pack(side="top", fill="x", expand=False, pady=1)
        self._details_content_scroll.pack(fill="both", expand=True, pady=1)
        self._details_title_lb.pack(side="left", padx=4)
        self._details_count_lb.pack(side="left", padx= 5)

    @property
    def left_entry(self):
        return self._left_entry

    @property
    def right_entry(self):
        return self._right_entry

    @property
    def top_combobox(self):
        return self._top_lang

    @property
    def bottom_combobox(self):
        return self._bottom_lang

    @property
    def trans_btn(self):
        return self._trans_bt

    @property
    def details_count_lb(self):
        return self._details_count_lb

    @property
    def details_content_frame(self):
        return self._details_content_frame



if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x500")
    root.title("Exemple TraductionStack")

    frame = TranslationFrame(root)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    root.mainloop()
