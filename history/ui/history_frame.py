import tkinter
import os
from tkinter import Frame, Misc
from tkinter.ttk import Label, Combobox, Button

from shared.infra.utils.image_utils import ImageUtils
from shared.ui.components.advanced_spin_box import AdvancedSpinBox
from shared.ui.components.scroll_pane import ScrollPane


class HistoryFrame(Frame):
    _FIRST_PAGE_IMG_PATH = os.path.join(os.path.dirname(__file__),"../resources/images/icons8-double-left-100.png")
    _LAST_PAGE_IMG_PATH = os.path.join(os.path.dirname(__file__),"../resources/images/icons8-double-right-100.png")
    _PREVIOUS_PAGE_IMG_PATH = os.path.join(os.path.dirname(__file__),"../resources/images/icons8-back-100.png")
    _NEXT_PAGE_IMG_PATH = os.path.join(os.path.dirname(__file__),"../resources/images/icons8-forward-100.png")
    #
    _CONFIG_BTN_SIZE = (15, 15)


    def __init__(self, master : Misc | None = None, **kwargs):
        super().__init__(master, **kwargs)
        #Image
        self._first_page_img = ImageUtils.image_file_to_tk_image(ImageUtils.get_image(self._FIRST_PAGE_IMG_PATH), self._CONFIG_BTN_SIZE)
        self._previous_page_img = ImageUtils.image_file_to_tk_image(ImageUtils.get_image(self._PREVIOUS_PAGE_IMG_PATH), self._CONFIG_BTN_SIZE)
        self._next_page_img = ImageUtils.image_file_to_tk_image(ImageUtils.get_image(self._NEXT_PAGE_IMG_PATH), self._CONFIG_BTN_SIZE)
        self._last_page_img = ImageUtils.image_file_to_tk_image(ImageUtils.get_image(self._LAST_PAGE_IMG_PATH), self._CONFIG_BTN_SIZE)


        #Title Frame
        self.title_frame = Frame(self, bg="light gray", height=75, padx=10, pady=4)
        self.title_frame.pack_propagate(False)
        #
        self.title = Label(self.title_frame, text="Historique", font=("Ubuntu", 24, "bold"), background=self.title_frame["bg"])
        self.history_selector = Combobox(self.title_frame, background=self.title_frame["bg"], width=12, font=("Ubuntu", 14), state="readonly")

        #Content Frame
        self.content_scroll = ScrollPane(self, bg="white")
        self.content_pane = Frame(self.content_scroll.pane, bg="white")

        #Config Frame
        self.config_frame = Frame(self, bg="light gray", height=50, pady=2, padx=2)
        #
        self.page_frame = Frame(self.config_frame)
        self.displayed_frame = Frame(self.config_frame)
        #
        self.first_page_btn = Button(self.page_frame, image=self._first_page_img)
        self.previous_page_btn = Button(self.page_frame, image=self._previous_page_img)
        self.page_selection_spin = AdvancedSpinBox(self.page_frame, width=4, validate="all", font=("Ubuntu", 14))
        self.page_count_lb = Label(self.page_frame, width=2, font=("Ubuntu", 14))
        self.next_page_btn = Button(self.page_frame, image=self._next_page_img)
        self.last_page_btn = Button(self.page_frame, image=self._last_page_img)
        #
        self.displayed_spin = AdvancedSpinBox(self.displayed_frame, width=4, validate="all", font=("Ubuntu", 14))

        #title frame
        self.title_frame.pack(fill="x", side="top")
        self.title.pack(side="left", anchor="w")
        #
        self.history_selector.pack(side="right", anchor="e")

        #content frame
        self.content_scroll.pack(fill="both", expand=True)
        self.content_pane.pack(fill="both", expand=True)

        #config frame
        self.config_frame.pack(fill="x", side="top")
        #
        self.page_frame.pack(side="left")
        #
        Label(self.page_frame, text="Page", font=("", 11, "bold")).pack(side="left")
        self.first_page_btn.pack(padx=2, side="left")
        self.previous_page_btn.pack(padx=2, side="left")
        self.page_selection_spin.pack(padx=2, side="left")
        Label(self.page_frame, text="/").pack(padx=2, side="left")
        self.page_count_lb.pack(padx=2, side="left")
        self.next_page_btn.pack(padx=2, side="left")
        self.last_page_btn.pack(padx=2, side="left")
        #
        self.displayed_frame.pack(side="right")
        #
        Label(self.displayed_frame, text="Lots de", font=("", 11, "bold")).pack(side="left")
        self.displayed_spin.pack(side="left", padx=2)

    def clear_content_frame(self):
        for c in self.content_pane.winfo_children(): c.destroy()

if __name__ == "__main__" :
    root = tkinter.Tk()
    root.title("history Frame")
    root.geometry("500x500")
    #
    frame = HistoryFrame(root)
    frame.pack(fill="both", expand=True)
    #
    root.mainloop()


