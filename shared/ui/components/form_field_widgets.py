import tkinter
from tkinter import Misc, BooleanVar, StringVar
from tkinter.ttk import Combobox, Checkbutton
from typing import Any, Tuple, List

from shared.domain.interfaces.form_field import FormField
from shared.infra.utils.validation_utils import validate_type
from shared.ui.components.advanced_entry import AdvancedEntry
from shared.ui.components.advanced_spin_box import IntSpinBox


class EntryField(AdvancedEntry, FormField):
    def __init__(
            self,
            master : Misc,
            name : str,
            text : str = "",
            placeholder : str | None = None,
            read_only = False,
            required : bool = True,
            **kwargs
    ):
        AdvancedEntry.__init__(self, master, text=text, placeholder=placeholder, **kwargs)
        FormField.__init__(self, name, required=required)
        #
        self.bind(self.TEXT_CHANGED, lambda _ : self._handler_on_changed())
        self._disable() if read_only else self._enable()

    def set(self, value: Any):
        self.text = value

    def get(self) -> Any:
        return self.text

    def _enable(self):
        self.configure(state='normal')

    def _disable(self):
        self.configure(state='readonly')

    def reset(self):
        self.text = ""


class ComboBoxField(Combobox, FormField):
    def __init__(
            self,
            master,
            name,
            read_only = False,
            required: bool = True,
            **kwargs
    ):
        Combobox.__init__(self, master, **kwargs)
        FormField.__init__(self, name, required=required)
        #
        self.bind("<<ComboboxSelected>>", lambda _: self._handler_on_changed())
        self._disable() if read_only else self._enable()

    def set(self, value):
        super().set(value)
        self._handler_on_changed()

    def _enable(self):
        self.configure(state='readonly')

    def _disable(self):
        self.configure(state='disabled')

    def reset(self):
        self.set("")

class ComboBoxValuesField(FormField):
    def reset(self):
        pass

    def __init__(
            self,
            name: str,
            host_combobox : Combobox
    ):
        super().__init__(name, required=False)
        self.host_combobox = host_combobox

    @property
    def host_combobox(self) -> Combobox:
        return self._host_combobox

    @host_combobox.setter
    def host_combobox(self, value : Combobox):
        validate_type(value, Combobox, "host_combobox")
        self._host_combobox = value

    def set(self, value: Tuple[str] | List[str]):
        if not isinstance(value, list | tuple) :
            raise TypeError(f"values must be list or tuple. got type {type(value).__name__}")
        #
        self._handler_on_changed()
        self.host_combobox.configure(values=value)

    def get(self) -> Tuple[str]:
        return self.host_combobox.cget("values")

    def _enable(self):
        pass

    def _disable(self):
        pass


class CheckBoxField(Checkbutton, FormField):
    def __init__(
            self,
            master : Misc,
            name : str,
            read_only = False,
            **kwargs
    ):
        Checkbutton.__init__(self, master, **kwargs)
        FormField.__init__(self, name, required=False)
        #
        self._state = BooleanVar(self, False)
        self.configure(variable=self._state, command=self._handler_on_changed)
        #
        self._disable() if read_only else self._enable()

    def set(self, value: bool):
        self._state.set(value)

    def get(self) -> Any:
        return self._state.get()

    def _enable(self):
        self.configure(state='normal')

    def _disable(self):
        self.configure(state='disabled')

    def reset(self):
        self._state.set(False)

class IntSpinBoxField(IntSpinBox, FormField):
    def __init__(self, master, name, read_only = False, required : bool = True, **kwargs):
        IntSpinBox.__init__(self, master, **kwargs)
        FormField.__init__(self, name, required)
        #
        self._text_var = StringVar(self, '0')
        self.configure(textvariable=self._text_var)
        self._text_var.trace_add('write', lambda x, y, z : self._handler_on_changed())
        self._disable() if read_only else self._enable()

    def _enable(self):
        self.configure(state='normal')

    def _disable(self):
        self.configure(state='readonly')

    def reset(self):
        self._text_var.set('0')


if __name__ == "__main__" :
    root = tkinter.Tk()
    root.geometry("500x400")
    entry = EntryField(root, "entry", "Nom", placeholder="Entrez votre texte ici...")
    entry.on_changed = lambda i : print(i)
    entry1 = EntryField(root, "entry", "Nom", placeholder="Entrez votre texte ici...", read_only=True)
    combobox = ComboBoxField(root, "btn", True, values=("1", "2", "3"))
    checkbutton = CheckBoxField(root, "check", False, text="Coche et décoche moi.")
    combobox.bind("<<ComboboxSelected>>", lambda e : print(e.widget.get()))
    checkbutton.on_changed = lambda i : print(i)
    spin = IntSpinBoxField(root, "spin", from_=0, to_ = 100)
    spin.on_changed = lambda i: print(i)
    spin.set(100)
    #
    entry.pack(fill='x', side='top', pady=2)
    entry1.pack(fill='x', side='top', pady=2)
    combobox.pack(fill='x', side='top', pady=2)
    checkbutton.pack(fill='x', side='top', pady=2)
    spin.pack(fill='x', side='top', pady=2)
    root.mainloop()