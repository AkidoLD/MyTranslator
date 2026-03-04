import tkinter
from tkinter import Widget, Button
from tkinter.ttk import Frame
from typing import Dict, Type

from shared.domain.interfaces.data_form import DataForm
from shared.infra.utils.validation_utils import validate_type_or_none
from shared.ui.components.stack_frame import StackFrame
from shared.ui.components.titled_frame import TitledFrame
from translation.ui.components.provider_advanced_data_form import ProviderAdvancedDataForm, ExecProviderAdvancedDataForm
from translation.ui.components.provider_basic_data_form import ProviderBasicDataForm


class ProviderDataForm(Frame, DataForm):
    BASIC_DATA_FORM = "provider_basic_data_form"
    ADVANCED_DATA_FORM = "provider_advanced_data_form"

    def __init__(
            self,
            master,
            provider_advanced_data_forms : Dict[str, Type[DataForm]] = None,
            **kwargs):
        Frame.__init__(self, master, **kwargs)
        DataForm.__init__(self)
        #
        self._build_ui()
        self._set_style()
        #
        self.advanced_data_forms = provider_advanced_data_forms or {}
        self._basic_data_form.on_provider_type_field_changed = self._advanced_data_stack.raise_item

    def _set_advanced_data_forms(self, advanced_forms : Dict[str, Type[ProviderAdvancedDataForm]]):
        if not validate_type_or_none(advanced_forms, dict, "advanced_forms") : return
        # Set default type
        keys = tuple(advanced_forms.keys())
        self._basic_data_form.set_field(ProviderBasicDataForm.PROVIDER_TYPE_VALUES_FIELD, keys)
        #
        self._advanced_data_stack.clear()  # Clear previous advanced forms
        #
        for k, v in advanced_forms.items():
            self._advanced_data_stack.add_item(k, v, name=self.ADVANCED_DATA_FORM)
        #
        self._advanced_data_stack.raise_item(keys[0])

    def _build_ui(self):
        basic_form_titled_pane =  TitledFrame(self, "Basique")
        self._basic_form_pane = basic_form_titled_pane.pane
        #
        advanced_form_titled_pane = TitledFrame(self, "Avancé", height=100)
        self._advanced_form_pane = advanced_form_titled_pane.pane
        self._advanced_data_stack = StackFrame(
            self,
            on_item_raised=self._on_raised_advanced_form_changed
        )
        #
        self._basic_data_form = ProviderBasicDataForm(self._basic_form_pane, self.BASIC_DATA_FORM)

        #
        basic_form_titled_pane.pack(side='top', fill='x', pady=4)
        advanced_form_titled_pane.pack(side='top', fill='x', pady=4)
        self._advanced_data_stack.pack(fill='both', expand=True, padx=2)
        #
        self._basic_data_form.pack(fill='both', expand=True, padx=2)
        #
        self._set_form_field(self.BASIC_DATA_FORM, self._basic_data_form)

    def _set_style(self):
        pass

    def is_valid(self):
        return self.basic_data_form.is_valid() and self.advanced_data_form.is_valid()

    def _on_raised_advanced_form_changed(self, name):
        self._set_form_field(self.ADVANCED_DATA_FORM, self.advanced_data_form)
        self.basic_data_form.set_field(ProviderBasicDataForm.PROVIDER_TYPE_FIELD, name)

    @property
    def basic_data_form(self):
        return self._basic_data_form

    @property
    def advanced_data_form(self) -> ProviderAdvancedDataForm:
        return validate_type_or_none(self._advanced_data_stack.raised_item, DataForm, "advanced_data_form")

    @property
    def advanced_data_forms(self) -> Dict[str, Widget]:
        return self._advanced_data_stack.inserted_items

    @advanced_data_forms.setter
    def advanced_data_forms(self, values: Dict[str, Type[ProviderAdvancedDataForm]]):
        self._set_advanced_data_forms(values)

if __name__ == "__main__":
    root = tkinter.Tk()
    root.geometry("500x500")
    central = ProviderDataForm(root, {"binary" : ExecProviderAdvancedDataForm})
    central.pack(fill='both', expand=True)
    central.set_field(ProviderDataForm.BASIC_DATA_FORM,{"provider_id" : "23123asd121"})
    Button(root, text="get data", command=lambda : print(central.is_valid(), central.get())).pack(side='bottom', fill='x')
    root.mainloop()