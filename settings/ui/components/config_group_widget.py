import os.path
import tkinter
from tkinter import Event
from tkinter.ttk import Button, Frame, Style

from settings.ui.components.config_button import ConfigButton
from shared.infra.utils.image_utils import ImageUtils


class ConfigGroupWidget(Frame):
    _TOGGLE_BTN_IMG_PATH = os.path.join(os.path.dirname(__file__), "../../resources/icons8-expand-arrow-100.png")
    _TOGGLE_BTN_IMG_SIZE = (22, 22)
    def __init__(self, master, text : str, **kwargs):
        super().__init__(master, **kwargs)
        #Style
        font = ("Arial", 14, "bold")

        Style().configure(
            "ConfigGroupWidget.TButton",
            background="#b2b2b2",
            forground="black",
            font=font,
            anchor="w",
            space=10,
            padding=(10, 2)
        )
        #
        Style().map(
            "ConfigGroupWidget.TButton",
            background=[
                ("active", "gray"),
                ("pressed", "#dddddd"),
                ("disabled", "#dddddd")
            ],
            forground=[
                ("disabled", "white")
            ]
        )
        #
        self._un_dropped_img = ImageUtils.get_tk_image(self._TOGGLE_BTN_IMG_PATH, self._TOGGLE_BTN_IMG_SIZE, 90)
        self._dropped_img = ImageUtils.get_tk_image(self._TOGGLE_BTN_IMG_PATH, self._TOGGLE_BTN_IMG_SIZE)
        #
        self._toggle_btn = Button(self, style="ConfigGroupWidget.TButton", compound="right", image=self._un_dropped_img)
        self._config_btn_frame = Frame(self, padding=(0, 0, 0, 2))
        #
        self.text = text
        self._is_dropped = False
        #
        self._toggle_btn.pack(side="top", fill="x", pady=1, padx=1)

        #
        self._toggle_btn.bind("<Button-1>", self._on_toggle_btn_clicked)

    def _toggle_btn_frame(self):
        self.pane.pack_forget() if self._is_dropped else self.pane.pack(side="top", fill="both")
        self._is_dropped = not self._is_dropped
        #
        self._toggle_btn.config(image=self._dropped_img if self._is_dropped else self._un_dropped_img)
        #

    def _on_toggle_btn_clicked(self, _ : Event):
        self.after(200, self._toggle_btn_frame)

################################## GETTERS AND SETTERS ######################################
    @property
    def text(self):
        return self._toggle_btn.cget("text")

    @text.setter
    def text(self, value : str):
        if not isinstance(value, str):
            raise TypeError(f"text must be str, got type {type(value).__name__}.")
        #
        if not value.strip():
            raise ValueError("text can't be empty.")
        #
        self._toggle_btn.config(text=value)

    @property
    def btn(self):
        return self._toggle_btn

    @property
    def pane(self):
        return self._config_btn_frame

if __name__ == "__main__":
    root = tkinter.Tk()
    root.geometry("500x500")
    frame = Frame(root)
    #
    config_1 = ConfigGroupWidget(frame, text="Config Group 1")
    config_2 = ConfigGroupWidget(config_1.pane, text="Config Group 2")
    #
    config_2.pack(side="top", fill="x")
    ConfigButton(config_1.pane, text="Test configuration 1").pack(side="top", fill='x')
    ConfigButton(config_1.pane, text="Test configuration 2").pack(side="top", fill='x')
    ConfigButton(config_2.pane, text="Test configuration 1").pack(side="top", fill='x')
    config_1.pack(side="top", fill="x")
    #
    frame.pack(fill="both", expand=True)

    root.mainloop()
