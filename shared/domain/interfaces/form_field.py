from abc import ABC, abstractmethod
from typing import Any, Callable

from shared.infra.utils.validation_utils import validate_type, validate_not_empty, validate_callable


class FormField(ABC):
    def __init__(
            self,
            name : str,
            required : bool = True,
            on_changed : Callable[[Any], None] = None
    ):
        #
        super().__init__()
        self.name = name
        self.required = required
        self.on_changed = on_changed
        #
        self._readonly = False

    @property
    def name(self): return self._name

    @name.setter
    def name(self, value : str):
        self._name = validate_not_empty(validate_type(value, str, "name"), "name")

    @property
    def required(self): return self._required

    @required.setter
    def required(self, value):
        self._required = validate_type(value, bool, 'required')

    @property
    def on_changed(self) -> Callable[[Any], None]: return self._on_changed

    @on_changed.setter
    def on_changed(self, value : Callable[[Any], None]):
        self._on_changed = validate_callable(value, "on_changed")

    def set_readonly(self, value : bool):
        self._readonly = validate_type(value, bool, "readonly")
        self._disable() if value else self._enable()

    def get_read_only(self) -> bool:
        return self._readonly

    @property
    def readonly(self):
        return self._readonly

    @readonly.setter
    def readonly(self, value):
        self.set_readonly(value)

    @abstractmethod
    def set(self, value : Any):pass

    @abstractmethod
    def get(self) -> Any: pass

    @abstractmethod
    def _enable(self): pass

    @abstractmethod
    def _disable(self): pass

    @abstractmethod
    def reset(self): pass

    def is_valid(self) -> bool:
        return True if not self.required or bool(self.get()) else False

    def _handler_on_changed(self):
        if self.on_changed : self.on_changed(self.get())