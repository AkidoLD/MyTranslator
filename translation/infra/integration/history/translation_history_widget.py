import os
import tkinter
from datetime import datetime
from tkinter import Frame, Misc, font, Button
from tkinter.ttk import Label, Style


from history.domain.interfaces.history_entry_widget import HistoryEntryWidget
from shared.infra.utils.image_utils import ImageUtils
from shared.ui.components.bordered_frame import BorderedFrame
from shared.ui.components.clipboard_button import ClipboardButton
from shared.ui.mixins.smart_events import SmartEventMixin


class TranslationHistoryWidget(HistoryEntryWidget, SmartEventMixin, Frame) :
    _TOWARD_ICON_PATH = os.path.join(os.path.dirname(__file__), "../../../resources/icons8-arrow-100.png")
    _BORDER_COLOR = "black"
    _BACKGROUND_COLOR = "light yellow"
    _TIME_COLOR = "white"

    def __init__(
            self,
            master : Misc,
            original_text : str,
            translated_text : str,
            src_lang : str,
            target_lang : str,
            trans_date : datetime,
            **kwargs
    ):
        super().__init__(master, **kwargs)
        #
        self.config(pady=1, padx=1, background=master["bg"])
        #
        Style().configure(
            "Text.TLabel",
            background=self._BACKGROUND_COLOR,
            font=("Ubuntu", 13),
            wraplength=250
        )

        Style().configure(
            "Lang.TLabel",
            background=self._BACKGROUND_COLOR,
            font=("Arial", 16, "bold"),
        )

        Style().configure(
            "Time.TLabel",
            background=self._BORDER_COLOR,
            foreground=self._TIME_COLOR,
            font=("Ubuntu", 11, "bold"),
            padding=(10, 2)
        )

        self._was_horizontal = None
        #
        self._img = ImageUtils.get_image(self._TOWARD_ICON_PATH, size=(50, 50))
        self._toward_image_0 = ImageUtils.convert_to_tk_image(self._img, size=(20, 20))
        self._toward_image_90 = ImageUtils.convert_to_tk_image(self._img, size=(20, 20), rotation=-90)

        #Content Frame
        self._bordered_frame = BorderedFrame(self, background=self._BACKGROUND_COLOR, border=2, border_color=self._BORDER_COLOR)
        self._main_frame = self._bordered_frame.pane
        self._main_frame.configure(padx=10, pady=15)
        #
        self._text_frame = Frame(self._main_frame, bg=self._BACKGROUND_COLOR)
        self._lang_frame = Frame(self._main_frame, bg=self._BACKGROUND_COLOR)
        #
        self._original_text_lb = Label(self._text_frame, text=original_text, style="Text.TLabel")
        self._toward_lb = Label(self._text_frame, image=self._toward_image_0, style="Text.TLabel")
        self._translated_text_lb = Label(self._text_frame, text=translated_text, style="Text.TLabel")
        #
        self._src_lang_lb = Label(self._lang_frame, text=src_lang, style="Lang.TLabel")
        self._target_lang_lb = Label(self._lang_frame, text=target_lang, style="Lang.TLabel")
        self._copy_btn = ClipboardButton(self._lang_frame, self._translated_text_lb.cget("text"), size=35, relief="flat", bg=self._BACKGROUND_COLOR)
        #
        self._trans_date = Label(self, text=trans_date.strftime("%d/%m/%Y à %H:%M:%S"), style="Time.TLabel")
        #

        #Packing
        self._bordered_frame.pack(side="top", fill="both", expand=True)
        #
        self._text_frame.pack(side="left", fill="both", expand=True)
        self._lang_frame.pack(side="right", anchor="e")
        #
        self._update_text_frame_layout()
        #
        self._src_lang_lb.pack(side="left")
        Label(self._lang_frame, image=self._toward_image_0, style="Lang.TLabel").pack(side="left", padx=7)
        self._target_lang_lb.pack(side="left")
        #
        self._copy_btn.pack(side="left", anchor="e", padx=(10, 0))
        #
        self._trans_date.pack(side="top", anchor="e")

        #
        self.bind("<Configure>", lambda _ : self._update_text_frame_layout())

    def _update_text_frame_layout(self):
        #Layout rule.
        req_width = 0
        for w in self._text_frame.winfo_children():
            req_width += w.winfo_reqwidth()
        #
        self.update()
        dispo_width = self._main_frame.winfo_width() - self._lang_frame.winfo_reqwidth()
        #
        is_horizontal = True if req_width <=  dispo_width else False
        if not is_horizontal :
            for w in self._text_frame.winfo_children():
                if isinstance(w, Label):
                    w.configure(wraplength=dispo_width - 50)
        #
        if self._was_horizontal is not None and self._was_horizontal == is_horizontal : return
        self._was_horizontal = is_horizontal
        #
        side = "left" if is_horizontal  else "top"
        image = self._toward_image_0 if is_horizontal else self._toward_image_90
        #
        self._original_text_lb.pack(side=side, anchor="center",padx=2, pady=2)
        self._toward_lb.pack(side=side, padx=2, anchor="center", pady=2)
        self._toward_lb.config(image=image)
        self._translated_text_lb.pack(side=side, anchor="center", padx=2, pady=2)



if __name__ == "__main__" :
    root = tkinter.Tk()
    root.geometry("400x400")
    frame = Frame(root, bg="white")

    history = TranslationHistoryWidget(
        frame,
        "Bonjour, je m'appelle Wouagang Sakam Rayen Alex (AkidoLD) et je suis programmeur.",
        "Hello, my _name_lb is Wouagang Sakam Rayen Alex (AkidoLD) and I am a programmer",
        "fr",
        "en",
        datetime.now()
    )

    frame.pack(side="top", fill="both", expand=True)
    history.pack(side="top", fill="x", expand=True)

    root.mainloop()

