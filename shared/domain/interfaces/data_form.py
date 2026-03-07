from abc import ABC
from typing import Dict, Any, Callable

from shared.domain.interfaces.form_field import FormField
from shared.infra.utils.validation_utils import validate_type, validate_callable


class DataForm(ABC):
    def __init__(
            self,
            on_field_changed : Callable[[str, Any], None] = None
    ):
        #
        self._form_fields : Dict[str, FormField] = {}
        self.on_field_changed = on_field_changed
        #
        self._readonly = False

    def _field_exist(self, name) -> bool:
        return name in self._form_fields

    def _register_field(self, field : FormField):
        if self._field_exist(field.name) :
            raise RuntimeError(f"field with the name {field.name} already exist.")
        #
        self._set_form_field(field.name, validate_type(field, FormField, "form_field"))

    def _unregister_field(self, name : str):
        if not self._form_fields.pop(name, None):
            raise RuntimeError(f"No field with the name {name}.")

    def _get_form_field(self, name: str) -> FormField:
        return self._form_fields.get(name, None)

    def _set_form_field(self, name, field : FormField):
        if self._field_exist(name) :
            print(f"Field with name {name} already exist. The value will be overwritten")
        #
        self._form_fields[name] = validate_type(field, FormField, "form_field")
        field.on_changed = lambda v : self._handler_on_field_changed(name, v)

    def get(self) -> Dict[str, Any]:
        return {name : field.get() for name, field in self._form_fields.items()}

    def set(self, data : Dict[str, Any]):
        for n, v in data.items(): self.set_field(n, v)

    def get_field(self, name : str) -> Any:
        if not self._field_exist(name):
            raise RuntimeError(f"Unable to get field data. No field with name {name} found")
        #
        return self._form_fields[name].get()

    def set_field(self, name : str, value : Any):
        if not self._field_exist(name):
            raise RuntimeError(f"Unable to set field data. No field with name {name} found")
        #
        self._form_fields[name].set(value)

    def set_readonly(self, value : bool):
        if value == self._readonly : return
        #
        self._readonly = validate_type(value, bool, "readonly")
        for field in self._form_fields.values(): field.readonly = value

    def get_readonly(self) -> bool:
        return self._readonly

    @property
    def readonly(self) -> bool:
        return self.get_readonly()

    @readonly.setter
    def readonly(self, value : bool):
        self.set_readonly(value)

    def set_field_readonly(self, name, value : bool):
        field = self._get_form_field(name)
        #
        field.readonly = value

    def reset(self):
        for field in self._form_fields.values() : field.reset()

    def is_valid(self):
        return all(field.is_valid() for field in self._form_fields.values())

    def _handler_on_field_changed(self, name : str, value : Any):
        if self.on_field_changed : self.on_field_changed(name, value)

    @property
    def on_field_changed(self) -> Callable[[str, Any], None]:
        return self._on_field_changed

    @on_field_changed.setter
    def on_field_changed(self, value : Callable[[str, Any], None]):
        self._on_field_changed = validate_callable(value, "on_field_changed")
