import tkinter
from tkinter.ttk import Label, Style, Frame
from typing import Tuple

from shared.infra.utils.validation_utils import validate_type, validate_not_empty
from shared.ui.components.circle_widget import CircleWidget
from shared.ui.mixins.smart_events import SmartEventMixin

class ProviderInternetReqCircle(CircleWidget):
    def __init__(self, master, req_internet, **kwargs):
        super().__init__(master, **kwargs)
        #
        self.req_internet = req_internet

    @property
    def req_internet(self):
        return self._req_internet

    @req_internet.setter
    def req_internet(self, value: bool):
        if value is None:
            self._req_internet = None
            self.color = "#f7f7f7"
        else:
            self._req_internet = validate_type(value, bool, "req_internet")
            self.color = "#4de14a" if value else "#529ee1"

class ProviderComboboxItem(Frame, SmartEventMixin):
    def __init__(
            self,
            master,
            p_id : str,
            name : str,
            req_internet : bool,
            background : str = "white",
            font : Tuple[str, int] | Tuple[str, int, str] = ("Ubuntu", 11, "bold"),
            **kwargs
    ):
        Frame.__init__(
            self,
            master,
            style="ProviderComboboxItem.TFrame",
            cursor="hand2",
            padding=2,
            **kwargs
        )
        SmartEventMixin.__init__(self)
        #
        self._p_id = validate_not_empty(validate_type(p_id, str, "provider_id"), "provider_id")
        self._req_internet = validate_type(req_internet, bool, "req_internet")
        #
        self._name_label = Label(
            self,
            text=validate_not_empty(validate_type(name, str, "name"), "name"),
            style="NameLabel.ProviderComboboxItem.TLabel",
            font=font
        )
        self._req_internet_cl = ProviderInternetReqCircle(
            self,
            req_internet,
            diameter=15,
            width=1,
            outline="black",
            background=background
        )
        #
        self._req_internet_cl.pack(side='right', fill='both')
        self._name_label.pack(side='left', fill='both', expand=True)
        #
        style = Style()
        _h_color = "#f7f7f7"
        style.configure("ProviderComboboxItem.TFrame", background=background, relief="sunken", borderwidth=1)
        style.map("ProviderComboboxItem.TFrame", background=[("active", _h_color)], relief=[("active", "solid")])
        #
        style.configure("NameLabel.ProviderComboboxItem.TLabel", background=background)
        style.map("NameLabel.ProviderComboboxItem.TFrame", background=[("active", _h_color)])
        #
        def _on_enter(_):
            self.state(["active"])
            self._name_label.state(["active"])
            self._req_internet_cl.configure(background=_h_color)

        def _on_leave(_):
            self.state(["!active"])
            self._name_label.state(["!active"])
            self._req_internet_cl.configure(background="white")
        #
        self.bind(self.SMART_ENTER, _on_enter)
        self.bind(self.SMART_LEAVE, _on_leave)

    def get(self):
        return self._p_id, self._name_label.cget('text'), self._req_internet

if __name__ == "__main__":
    root = tkinter.Tk()
    root.config(background="white")
    root.geometry("500x700")
    #
    item = ProviderComboboxItem(root, "1", "provider 1", True)
    item.pack(side='top', fill='x')
    root.mainloop()
