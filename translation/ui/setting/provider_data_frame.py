import os.path
import tkinter
from tkinter import Frame, BooleanVar
from tkinter.ttk import Button, Label, Checkbutton, Style
from typing import Callable, Dict, Type

from shared.infra.utils.image_utils import ImageUtils
from shared.infra.utils.validation_utils import validate_callable
from shared.ui.components.scroll_pane import ScrollPane
from translation.ui.components.provider_advanced_data_form import ProviderAdvancedDataForm, ExecProviderAdvancedDataForm
from translation.ui.components.provider_data_form import ProviderDataForm


class ProviderDataFrame(Frame):
    _EDIT_IMG_PATH = os.path.join(os.path.dirname(__file__), "../../resources/icons8-edit-pencil-100.png")
    _SAVE_IMG_PATH = os.path.join(os.path.dirname(__file__), "../../resources/icons8-save-100.png")
    _BACK_IMG_PATH = os.path.join(os.path.dirname(__file__), "../../resources/icons8-back-100.png")
    #

    def __init__(
            self,
            master,
            advanced_data_forms : Dict[str, Type[ProviderAdvancedDataForm]] = None,
            on_save_btn_clicked : Callable[[], None] = None,
            on_back_btn_clicked: Callable[[], None] = None,
            **kwargs
    ):
        super().__init__(master, **kwargs)
        #
        self._edit_btn_state = BooleanVar(self, False)
        #
        img_size = 30
        self._back_img = ImageUtils.get_tk_image(self._BACK_IMG_PATH, img_size)
        self._save_img = ImageUtils.get_tk_image(self._SAVE_IMG_PATH, img_size)
        self._edit_img = ImageUtils.get_tk_image(self._EDIT_IMG_PATH, img_size)
        #
        self.on_save_btn_clicked = on_save_btn_clicked
        self.on_back_btn_clicked = on_back_btn_clicked
        #
        self._build_ui()
        self._set_style()
        self._bind_events()
        #
        self.advanced_data_forms = advanced_data_forms
        self._provider_data_form.read_only(True)
        self.hide_save_btn()

    def _build_ui(self):
        title_pane = Frame(self, height=50)
        title_pane.pack_propagate(False)
        self._back_btn = Button(
            title_pane,
            image=self._back_img,
            cursor='hand2',
            style="BackButton.ProviderDataFrame.TButton",
            takefocus=0
        )
        #
        title_label = Label(title_pane, text="Informations du fournisseur", font=("Ubuntu", 18, "bold"))
        #
        option_pane = Frame(title_pane)
        self._edit_data_btn = Checkbutton(
            option_pane,
            image=self._edit_img,
            cursor='hand2',
            style='EditButton.ProviderDataFrame.Toolbutton',
            variable=self._edit_btn_state,
            takefocus=0
        )
        #
        self._save_data_btn = Button(
            option_pane,
            image=self._save_img,
            cursor='hand2',
            style="SaveButton.ProviderDataFrame.TButton",
            takefocus=0
        )
        #
        provider_data_scroll = ScrollPane(self)
        self._provider_data_form = ProviderDataForm(provider_data_scroll.pane)

        #
        title_pane.pack(side='top', fill='x')
        self._back_btn.pack(side='left', padx=5, fill='x')
        title_label.pack(side='left', fill='x', padx=2)
        option_pane.pack(side='right', padx=4)
        self._edit_data_btn.pack(side='left', padx=3, fill='both')
        self._save_data_btn.pack(side='left', padx=3, fill='both')
        #
        provider_data_scroll.pack(side='top', fill='both', expand=True)
        self._provider_data_form.pack(fill='both', expand=True)

    def _set_style(self):
        self.config()
        Style().configure(
            "BackButton.ProviderDataFrame.TButton",
            relief="flat",
            background="white",
            borderwidth=1,
            padding=0
        )
        #
        Style().configure("SaveButton.ProviderDataFrame.TButton", background="white", relief='flat')
        Style().map(
            "SaveButton.ProviderDataFrame.TButton",
            background=[
                ("pressed", "#f5ff89"),
                ("active", "#fbffd1"),
            ]
            ,
            relief=[
                ("pressed", "sunken"),
                ("active", "flat"),
            ]
        )
        #
        Style().configure('EditButton.ProviderDataFrame.Toolbutton', relief="flat", background="white", padding=(3,0))
        Style().map(
            "EditButton.ProviderDataFrame.Toolbutton",
            background=[
                ('selected', "#c8ceff"),
                ("active", "#dbe0ff"),
            ],
            relief=[
                ('selected', "sunken"),
                ("active", "flat"),
            ]
        )

    def _bind_events(self):
        self._edit_data_btn.config(command=self._handler_on_edit_btn_clicked)
        self._save_data_btn.config(command=self._handler_on_save_btn_clicked)
        self._back_btn.config(command=self._handler_on_back_btn_clicked)

    def show_save_btn(self):
        self._save_data_btn.pack(side='left', expand=True)

    def hide_save_btn(self):
        self._save_data_btn.pack_forget()

    # -- Handler ---------------------------------------------
    def _handler_on_save_btn_clicked(self):
        if self.on_save_btn_clicked : self.on_save_btn_clicked()

    def _handler_on_edit_btn_clicked(self):
        self._provider_data_form.read_only(not self._edit_btn_state.get())

    def _handler_on_back_btn_clicked(self):
        if self.on_back_btn_clicked : self.on_back_btn_clicked()

    #-- Getter and Setter ------------------------------------
    def get_form_data(self):
        return self._provider_data_form.get()

    def set_form_data(self, value):
        self._provider_data_form.set(value)

    @property
    def form_data(self):
        return self.get_form_data()

    @form_data.setter
    def form_data(self, value):
        self.set_form_data(value)

    @property
    def on_save_btn_clicked(self):
        return self._on_save_btn_clicked
    
    @on_save_btn_clicked.setter
    def on_save_btn_clicked(self, value):
        self._on_save_btn_clicked = validate_callable(value, "on_save_btn_clicked")

    @property
    def on_back_btn_clicked(self):
        return self._on_back_btn_clicked

    @on_back_btn_clicked.setter
    def on_back_btn_clicked(self, value):
        self._on_back_btn_clicked = validate_callable(value, "on_back_btn_clicked")

    @property
    def advanced_data_forms(self):
        return self._provider_data_form.advanced_data_forms

    @advanced_data_forms.setter
    def advanced_data_forms(self, value):
        self._provider_data_form.advanced_data_forms = value

if __name__ == "__main__" :
    root = tkinter.Tk()
    root.geometry("500x400")
    #
    view = ProviderDataFrame(
        root,
        advanced_data_forms={"binary" : ExecProviderAdvancedDataForm},
        on_save_btn_clicked=lambda : print(view.form_data)
    )
    view.show_save_btn()

    view.pack(fill='both', expand=True)
    #
    root.mainloop()