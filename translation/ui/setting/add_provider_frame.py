import os
import tkinter
from tkinter import Frame, messagebox
from tkinter.ttk import Button, Label, Style
from typing import Type, Dict, Callable

from shared.infra.services.tk_dialog_service import TkDialogService
from shared.infra.utils.image_utils import ImageUtils
from shared.infra.utils.validation_utils import validate_callable
from shared.ui.components.scroll_pane import ScrollPane
from translation.ui.components.provider_advanced_forms.exec_provider_advanced_data_form import ProviderAdvancedDataForm, ExecProviderAdvancedDataForm
from translation.ui.components.provider_data_form import ProviderDataForm


class AddProviderFrame(Frame, TkDialogService):
    _RESET_IMG_PATH = os.path.join(os.path.dirname(__file__), "../../resources/icons8-restart-100.png")
    _ADD_IMG_PATH = os.path.join(os.path.dirname(__file__), "../../resources/icons8-plus-math-100.png")
    _BACK_IMG_PATH = os.path.join(os.path.dirname(__file__), "../../resources/icons8-back-100.png")

    def __init__(
            self,
            master,
            advanced_data_forms : Dict[str, Type[ProviderAdvancedDataForm]] = None,
            on_back_btn_clicked : Callable[[], None] = None,
            on_add_btn_clicked : Callable[[], None] = None,
            on_reset_btn_clicked : Callable[[], None] = None,
            **kwargs
    ):
        super().__init__(master, **kwargs)
        #
        img_size = 30
        self._back_img = ImageUtils.get_tk_image(self._BACK_IMG_PATH, img_size)
        self._add_img = ImageUtils.get_tk_image(self._ADD_IMG_PATH, img_size)
        self._reset_img = ImageUtils.get_tk_image(self._RESET_IMG_PATH, img_size)
        #
        self.on_back_btn_clicked = on_back_btn_clicked
        self.on_add_btn_clicked = on_add_btn_clicked
        self.on_reset_btn_clicked = on_reset_btn_clicked
        #
        self._build_ui()
        self._set_style()
        self._bind_events()
        #
        self.advanced_data_forms = advanced_data_forms
        #
        self._on_field_changed()

    def _build_ui(self):
        title_pane = Frame(self, height=50)
        title_pane.pack_propagate(False)
        #
        self._back_btn = Button(
            title_pane, image
            =self._back_img,
            padding=1,
            style="BackButton.AddProviderFrame.TButton",
            cursor="hand2",
            takefocus=0
        )
        title_lb = Label(title_pane, text="Ajouter Fournisseur", font=("Ubuntu", 18, "bold"))
        #
        option_pane = Frame(title_pane)
        self._reset_btn = Button(
            option_pane,
            image=self._reset_img,
            padding=1,
            style="ResetButton.AddProviderFrame.TButton",
            cursor="hand2",
            takefocus=0
        )
        self._add_btn = Button(
            option_pane,
            image=self._add_img,
            padding=1,
            style="AddButton.AddProviderFrame.TButton",
            cursor="hand2",
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
        title_lb.pack(side='left', fill='x', padx=2)
        #
        self._reset_btn.pack(side='left', padx=2, fill='both')
        self._add_btn.pack(side='left', padx=2, fill='both')
        #
        provider_data_scroll.pack(side='top', fill='both', expand=True)
        self.provider_data_form.pack(fill='both', expand=True)


    def _set_style(self):
        self.config()
        #
        Style().configure(
            'BackButton.AddProviderFrame.TButton',
            background="white",
            relief="flat",
            borderwidth=1
        )
        #
        Style().configure(
            'ResetButton.AddProviderFrame.TButton',
            background="white",
            relief="flat",
            borderwidth=1
        )
        #
        Style().configure(
            'AddButton.AddProviderFrame.TButton',
            background="white",
            relief="flat",
            borderwidth=1
        )
        Style().map(
            'AddButton.AddProviderFrame.TButton',
            background=[
                ("pressed", "#b0eaff"),
                ("active", "#caf1ff"),
            ]
        )

    def _bind_events(self):
        self._reset_btn.config(command=self._handler_on_reset_btn_clicked)
        self._add_btn.config(command=self._handler_on_add_btn_clicked)
        self._back_btn.config(command=self._handler_on_back_btn_clicked)


    def _on_field_changed(self, *_):
        self._show_add_btn() if self.provider_data_form.is_valid() else self._hide_add_btn()

    def _show_add_btn(self):
        self._add_btn.pack(side='left', padx=2, fill='both')

    def _hide_add_btn(self):
        self._add_btn.pack_forget()

    # -- Getter and Setter
    @property
    def on_reset_btn_clicked(self) -> Callable[[], None]:
        return self._on_reset_btn_clicked

    @on_reset_btn_clicked.setter
    def on_reset_btn_clicked(self, value : Callable[[], None]):
        self._on_reset_btn_clicked = validate_callable(value, "on_reset_btn_clicked")

    @property
    def advanced_data_forms(self):
        return self.provider_data_form.advanced_data_forms

    @advanced_data_forms.setter
    def advanced_data_forms(self, value):
        self.provider_data_form.advanced_data_forms = value

    @property
    def on_back_btn_clicked(self):
        return self._on_back_btn_clicked

    @on_back_btn_clicked.setter
    def on_back_btn_clicked(self, value):
        self._on_back_btn_clicked = validate_callable(value, "on_back_btn_clicked")

    @property
    def on_add_btn_clicked(self) -> Callable[[], None]:
        return self._on_add_btn_clicked

    @on_add_btn_clicked.setter
    def on_add_btn_clicked(self, value : Callable[[], None]):
        self._on_add_btn_clicked : Callable[[], None] = validate_callable(value, "on_add_btn_clicked")

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

    # -- Handler --------------------------------------------------
    def _handler_on_back_btn_clicked(self):
        if self.on_back_btn_clicked : self.on_back_btn_clicked()

    def _handler_on_reset_btn_clicked(self):
        if self.on_reset_btn_clicked : self.on_reset_btn_clicked()

    def _handler_on_add_btn_clicked(self):
        if not self.provider_data_form.is_valid():
            self.error_dialog("Erreur lors de la soumis du formulaire",
                              "Veuillez remplir tout les champs requis du formulaire.")
            return
        #
        if self.on_add_btn_clicked : self.on_add_btn_clicked()

if __name__ == "__main__" :
    root = tkinter.Tk()
    root.geometry("500x400")
    #
    view = AddProviderFrame(
        root,
        advanced_data_forms={"binary" : ExecProviderAdvancedDataForm, "http" : ExecProviderAdvancedDataForm},
        on_add_btn_clicked=lambda : print(view.form_data)
    )
    view.form_data = {ProviderDataForm.BASIC_DATA_FORM : {"provider_id": "asdasdasd"}}

    view.pack(fill='both', expand=True)
    #
    root.mainloop()