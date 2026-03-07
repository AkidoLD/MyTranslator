from abc import ABC
from tkinter.ttk import Frame
from typing import Any

from shared.domain.interfaces.data_form import DataForm
from shared.domain.interfaces.form_field import FormField


class ProviderAdvancedDataForm(Frame, DataForm, FormField, ABC):
    def __init__(
            self,
            master,
            name,
            required : bool = True,
            **kwargs
    ):
        Frame.__init__(self, master, **kwargs)
        FormField.__init__(self, name, required)
        DataForm.__init__(self)
        #
        self.on_changed = self.on_field_changed

    def _enable(self):
        self.readonly = False

    def _disable(self):
        self.readonly = True

    def _handler_on_field_changed(self, name : str, value : Any):
        self._handler_on_changed()
        super()._handler_on_field_changed(name, value)