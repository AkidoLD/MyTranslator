import os.path
import tkinter
from tkinter import Frame, BooleanVar
from tkinter.ttk import Button, Label, Checkbutton, Style
from typing import Callable, Dict, Type

from shared.infra.services.tk_dialog_service import TkDialogService
from shared.infra.utils.image_utils import ImageUtils
from shared.infra.utils.validation_utils import validate_callable, validate_type
from shared.ui.components.scroll_pane import ScrollPane
from translation.ui.components.provider_advanced_forms.exec_provider_advanced_data_form import ProviderAdvancedDataForm, ExecProviderAdvancedDataForm
from translation.ui.components.provider_data_form import ProviderDataForm


class UpdateProviderFrame(Frame, TkDialogService):
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
        self._readonly = False
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
        self._handler_on_edit_btn_clicked()
        #
        self._on_field_changed()

    def _build_ui(self):
        title_pane = Frame(self, height=50)
        title_pane.pack_propagate(False)
        self._back_btn = Button(
            title_pane,
            image=self._back_img,
            cursor='hand2',
            style="BackButton.UpdateProviderFrame.TButton",
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
            style='EditButton.UpdateProviderFrame.Toolbutton',
            variable=self._edit_btn_state,
            takefocus=0
        )
        #
        self._save_data_btn = Button(
            option_pane,
            image=self._save_img,
            cursor='hand2',
            style="SaveButton.UpdateProviderFrame.TButton",
            takefocus=0
        )
        #
        provider_data_scroll = ScrollPane(self)
        self.provider_data_form = ProviderDataForm(provider_data_scroll.pane)
        self.provider_data_form.on_field_changed = self._on_field_changed
        #
        option_pane.pack(side='right', padx=4)
        title_pane.pack(side='top', fill='x')
        self._back_btn.pack(side='left', padx=5, fill='x')
        title_label.pack(side='left', fill='x', padx=2)
        self._edit_data_btn.pack(side='left', expand=True, padx=3, fill='both')
        self._save_data_btn.pack(side='left', expand=True, padx=3, fill='both')
        #
        provider_data_scroll.pack(side='top', fill='both', expand=True)
        self.provider_data_form.pack(fill='both', expand=True)
        #

    def _set_style(self):
        self.config()
        Style().configure(
            "BackButton.UpdateProviderFrame.TButton",
            relief="flat",
            background="white",
            borderwidth=1,
            padding=0
        )
        #
        Style().configure("SaveButton.UpdateProviderFrame.TButton", background="white", relief='flat')
        Style().map(
            "SaveButton.UpdateProviderFrame.TButton",
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
        Style().configure('EditButton.UpdateProviderFrame.Toolbutton', relief="flat", background="white")
        Style().map(
            "EditButton.UpdateProviderFrame.Toolbutton",
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

    def _on_field_changed(self, *_):
        self._show_save_btn() if self.provider_data_form.is_valid() else self._hide_save_btn()

    def _show_save_btn(self):
        self._save_data_btn.pack(side='left', expand=True)

    def _hide_save_btn(self):
        self._save_data_btn.pack_forget()

    def set_readonly(self, status : bool):
        self._edit_btn_state.set(not status)
        self.provider_data_form.readonly = status

    @property
    def readonly(self):
        return self._readonly

    @readonly.setter
    def readonly(self, value):
        self._readonly = validate_type(value, bool, "readonly")
        self.set_readonly(value)

    # -- Handler ---------------------------------------------
    def _handler_on_save_btn_clicked(self):
        if self.on_save_btn_clicked : self.on_save_btn_clicked()

    def _handler_on_edit_btn_clicked(self):
        self.provider_data_form.readonly = not self._edit_btn_state.get()

    def _handler_on_back_btn_clicked(self):
        if self.on_back_btn_clicked : self.on_back_btn_clicked()

    #-- Getter and Setter ------------------------------------
    def get_form_data(self):
        return self.provider_data_form.get()

    def set_form_data(self, value):
        self.provider_data_form.set(value)

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
        return self.provider_data_form.advanced_data_forms

    @advanced_data_forms.setter
    def advanced_data_forms(self, value):
        self.provider_data_form.advanced_data_forms = value

if __name__ == "__main__" :
    root = tkinter.Tk()
    root.geometry("500x400")
    #
    view = UpdateProviderFrame(
        root,
        advanced_data_forms={"binary" : ExecProviderAdvancedDataForm, "http" : ExecProviderAdvancedDataForm},
        on_save_btn_clicked=lambda : print(view.form_data)
    )
    #
    view.pack(fill='both', expand=True)
    #
    root.mainloop()