import tkinter
from tkinter import Widget
from tkinter.ttk import Frame, Button
from typing import Dict, Type, Callable

from shared.infra.utils.validation_utils import validate_callable


class StackFrame(Frame):
    def __init__(
            self,
            master,
            on_item_raised : Callable[[str], None] = None,
            **kwargs
    ):
        super().__init__(master, **kwargs)
        #
        self.on_item_raised = on_item_raised
        #
        self._inserted_items : Dict[str, Widget] = {}
        self._raised_item : Widget | None = None
        #

    def add_item(self, item_id, widget : Type[Widget], **kwargs):
        if not issubclass(widget, Widget):
            raise TypeError(f"add_widget method wait a subclass of Widget, got type {widget.__name__}")
        #
        if item_id in self.inserted_items:
            raise ValueError(f"An item with id {item_id} already exist.")
        #
        item = widget(self, **kwargs)
        #
        self.inserted_items[item_id] = item
        if len(self.inserted_items) == 1 : self.raise_item(item_id)
        #
        return item

    def raise_item(self, item_id):
        item = self.inserted_items.get(item_id)
        if not item :
            raise ValueError(f"no item with id {item_id} found.")
        #
        if self.raised_item == item : return
        #
        if self.raised_item : self.raised_item.pack_forget()
        #
        item.pack(fill='both', expand=True)
        self._raised_item = item
        self._handler_on_item_raised(item_id)

    def remove_item(self, item_id):
        item = self.inserted_items.get(item_id)
        if not item :
            raise ValueError(f"No item with id {item_id}.")
        #
        del self.inserted_items[item_id]
        item.destroy()

    def clear(self):
        for w in self.inserted_items.values(): w.destroy()
        self._inserted_items = {}

    #--Handler ---------------------------------------------------------------------
    def _handler_on_item_raised(self, item_id : str):
        if self.on_item_raised : self.on_item_raised(item_id)

    #-- Getter and Setter ----------------------------------------------------------
    @property
    def on_item_raised(self) -> Callable[[str], None]:
        return self._on_item_raised

    @on_item_raised.setter
    def on_item_raised(self, value):
        self._on_item_raised = validate_callable(value, "on_item_raised")

    @property
    def raised_item(self) -> Widget:
        return self._raised_item

    @property
    def inserted_items(self) -> Dict[str, Widget]:
        return self._inserted_items



if __name__ == "__main__" :
    root = tkinter.Tk()
    root.geometry("500x400")
    #
    stack = StackFrame(root)
    frame1 = stack.add_item('frame1', Frame)
    frame2 = stack.add_item('frame2', Frame)
    #
    Button(frame1, text="Button frame 1", command=lambda : stack.raise_item('frame2')).pack(side='top', fill='x')
    Button(frame2, text="Button frame 2", command=lambda : stack.raise_item('frame1')).pack(side='top', fill='x')
    #
    stack.pack(fill='both', expand=True)
    root.mainloop()