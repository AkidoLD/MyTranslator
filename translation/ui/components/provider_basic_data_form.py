import tkinter
import uuid
from tkinter import Button
from tkinter.ttk import Frame, Label, Style
from typing import Tuple, Any, Callable

from shared.domain.interfaces.data_form import DataForm
from shared.domain.interfaces.form_field import FormField
from shared.infra.utils.validation_utils import validate_callable
from shared.ui.components.dict_view import DictView
from shared.ui.components.form_field_widgets import EntryField, CheckBoxField, ComboBoxField, IntSpinBoxField, \
    ComboBoxValuesField


class ProviderBasicDataForm(Frame, DataForm, FormField):
    PROVIDER_ID_FIELD = "provider_id"
    PROVIDER_NAME_FIELD = "provider_name"
    PROVIDER_TYPE_FIELD = "provider_type"
    PROVIDER_TYPE_VALUES_FIELD = "provider_type_values"
    PROVIDER_TIMEOUT_FIELD = "provider_timeout"
    PROVIDER_REQ_INTERNET_FIELD = "provider_req_internet"
    PROVIDER_DETECT_SRC_LANG_FIELD = "provider_detect_src_lang"
    PROVIDER_LANGUAGES_FIELD = "provider_languages"

    def __init__(
            self,
            master,
            name,
            font : Tuple[str, int] | Tuple[str, int, str] = ("", 11),
            on_type_field_changed : Callable[[str], None] = None,
            **kwargs
    ):
        Frame.__init__(self, master, **kwargs)
        FormField.__init__(self, name)
        DataForm.__init__(self)
        #
        self._font = font
        self.on_type_field_changed = on_type_field_changed
        #
        self._build_ui()
        self._reg_form_fields()
        self._set_style()
        self._bind_events()

    def _reg_form_fields(self):
        self._register_field(self._provider_id_entry)
        self._register_field(self._provider_name_entry)
        self._register_field(self._provider_req_internet_check_btn)
        self._register_field(self._provider_type_combobox)
        self._register_field(self._provider_type_combobox_values)
        self._register_field(self._provider_detect_src_lang_check_btn)
        self._register_field(self._provider_timeout_spin)
        self._register_field(self._provider_languages_widget)

    def _build_ui(self):
        self.configure(style='ProviderBasicDataForm.TFrame')
        #
        self._provider_id_entry = EntryField(
            self,
            self.PROVIDER_ID_FIELD,
            placeholder="ID du fournisseur ...",
            read_only=True,
            style="EntryField.ProviderBasicDataForm.TEntry",
            font=self._font,
            required=False
        )
        #
        self._provider_name_entry = EntryField(
            self,
            self.PROVIDER_NAME_FIELD,
            placeholder="Nom du fournisseur ...",
            style="EntryField.ProviderBasicDataForm.TEntry",
            font=self._font,
        )
        #
        self._provider_req_internet_check_btn = CheckBoxField(
            self,
            self.PROVIDER_REQ_INTERNET_FIELD,
            text="Require internet",
            style="TitleLabel.ProviderBasicDataForm.TCheckbutton",
            cursor="hand2"
        )
        #
        self._provider_type_combobox = ComboBoxField(
            self,
            self.PROVIDER_TYPE_FIELD,
            False,
            font=self._font
        )
        #
        self._provider_type_combobox_values = ComboBoxValuesField(
            self.PROVIDER_TYPE_VALUES_FIELD,
            self._provider_type_combobox
        )
        #
        self._provider_detect_src_lang_check_btn = CheckBoxField(
            self,
            self.PROVIDER_DETECT_SRC_LANG_FIELD,
            text="Détecte la langue source",
            style="TitleLabel.ProviderBasicDataForm.TCheckbutton",
            cursor = "hand2"
        )
        #
        self._provider_timeout_spin = IntSpinBoxField(
            self,
            self.PROVIDER_TIMEOUT_FIELD,
            to_ = 30,
            font=self._font
        )
        self._provider_languages_widget = DictView(self, "Langues", self.PROVIDER_LANGUAGES_FIELD, key_name="Nom",
                                                   value_name="Sigle", font=self._font)
        #
        Label(
            self,
            style="TitleLabel.ProviderBasicDataForm.TLabel",
            text="ID"
        ).grid(row=0, column=0, sticky='nswe')

        #
        self._provider_id_entry.grid(row=1, column=0, sticky='nswe')
        #
        Label(self, style="TitleLabel.ProviderBasicDataForm.TLabel", text="Nom").grid(row=2, column=0, sticky='nswe')
        self._provider_name_entry.grid(row=3, column=0, sticky='nswe')
        #
        Label(self, style="TitleLabel.ProviderBasicDataForm.TLabel", text="Type").grid(row=4, column=0, sticky='nswe')
        self._provider_type_combobox.grid(row=5, column=0, sticky='nswe')
        #
        self._provider_req_internet_check_btn.grid(row=6, column=0, sticky='nswe')
        #
        self._provider_detect_src_lang_check_btn.grid(row=7, column=0, sticky='nswe')
        #
        Label(self, style="TitleLabel.ProviderBasicDataForm.TLabel", text="Durée d'une traduction").grid(row=8, column=0, sticky='nswe')
        self._provider_timeout_spin.grid(row=9, column=0, sticky='nswe')
        #
        self._provider_languages_widget.grid(row=0, column=1, rowspan=10, columnspan=2, sticky='nswe')
        #
        self.grid_columnconfigure(0, weight=1, uniform='group')
        self.grid_columnconfigure(2, weight=1, uniform='group')

    def _set_style(self):
        self.configure()
        Style().configure("GeneralDataTitlePane.ProviderBasicDataForm.TFrame", background="#767679")
        Style().configure("GeneralDataTitleLabel.ProviderBasicDataForm.TLabel",
                          background="#767679",
                          foreground="black",
                          font=("Ubuntu", 18, "bold"))
        Style().configure("GeneralDataContentPane.ProviderBasicDataForm.TFrame",
                          background="white")
        #
        Style().configure("TitleLabel.ProviderBasicDataForm.TLabel",
                          font=("Ubuntu", 12, "bold"), padding=(1, 5, 1, 0))
        Style().configure("TitleLabel.ProviderBasicDataForm.TCheckbutton",
                          font=("Ubuntu", 11, "bold"), padding=(1, 5, 1, 0))

        Style().configure("EntryField.ProviderBasicDataForm.TEntry", fieldbackground="white")
        Style().map(
            "EntryField.ProviderBasicDataForm.TEntry",
            fieldbackground=[
                ("readonly", "light gray"),
                ("disabled", "light gray"),
                ("!readonly", "!disabled", "white"),
            ]
        )

    def _bind_events(self):
        pass

    def _handler_on_field_changed(self, name : str, value : Any):
        if name == self.PROVIDER_TYPE_FIELD : self._handler_on_type_field_changed()
        self._handler_on_changed()
        super()._handler_on_field_changed(name, value)

    def _enable(self):
        self.readonly = False

    def _disable(self):
        self.readonly = True

    def set_readonly(self, value):
        DataForm.set_readonly(self, value)
        self._provider_id_entry.readonly = True

    @property
    def on_type_field_changed(self) -> Callable[[str], None]:
        return self._on_type_field_changed

    @on_type_field_changed.setter
    def on_type_field_changed(self, value : Callable[[str], None]):
        self._on_type_field_changed = validate_callable(value, "on_type_field_changed")

    def _handler_on_type_field_changed(self):
        if self.on_type_field_changed : self.on_type_field_changed(self._provider_type_combobox.get())

if __name__ == "__main__":
    root = tkinter.Tk()
    root.geometry("500x500")
    central = ProviderBasicDataForm(root, "name")
    central.on_field_changed = lambda n, v : print(f"Field {n} changed to value : {v}")
    central.pack(fill="both", expand=True, padx=2, pady=2)
    Button(root, text="Récupérer donnees",command=lambda : print(central.get())).pack(side='bottom', fill='x')
    central.set_field("provider_id", str(uuid.uuid4()))
    central.on_provider_type_field_changed = lambda value : print(f"La nouvelle valeur est {value}")
    central.set_field(ProviderBasicDataForm.PROVIDER_LANGUAGES_FIELD, {"Francais" : "fr", "Anglais" : "en"})
    central.set_field(ProviderBasicDataForm.PROVIDER_TYPE_VALUES_FIELD, ("http", "binary", "lib"))
    root.after(5000, central.set_readonly, True)
    root.after(10000, central.set_readonly, False)
    print(Style().layout("TEntry"))
    print(Style().element_options("TEntry.field"))
    root.mainloop()
