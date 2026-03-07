import tkinter
from tkinter.ttk import Label, Style, Frame
from typing import Tuple

from shared.infra.utils.validation_utils import validate_type, validate_not_empty
from shared.ui.components.circle_widget import CircleWidget
from shared.ui.components.smart_frame import SmartFrame
from shared.ui.mixins.smart_events import SmartEventMixin


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
        self._req_internet_cl = CircleWidget(
            self,
            15,
            color= "#75ff73" if req_internet else "#75fdff",
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
