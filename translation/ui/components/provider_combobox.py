import tkinter as tk

from tkinter import Label, Frame, Event, StringVar, BooleanVar, Widget
from typing import List, Tuple, Dict

from shared.ui.components.circle_widget import CircleWidget
from shared.ui.components.float_menu import FloatFrame
from shared.ui.mixins.smart_events import SmartEventMixin


class ProviderInternetReqCircle(CircleWidget):
    def __init__(self, parent, req_internet : bool = False, diameter : float = 10,  **kwargs):
        super().__init__(parent, diameter, outline="", **kwargs)
        self.req_internet = req_internet

    @property
    def req_internet(self):
        return self._req_internet

    @req_internet.setter
    def req_internet(self, value):
        self._req_internet = value
        self.color = "green" if self._req_internet else "blue"

class ProviderReqInternetWidget(tk.Frame):
    def __init__(self, parent, req_internet=False, **kwargs):
        super().__init__(parent, **kwargs)
        #
        self._req_internet = req_internet
        self.req_internet_label = Label(self, bg=self["bg"], text=self._label_text(), font=("Ubuntu", 11, "bold"))
        self.req_internet_indicator = ProviderInternetReqCircle(self, req_internet, 15, bg=self["bg"])

        self.req_internet_label.pack(side="left")
        self.req_internet_indicator.pack(side="left", padx=2)

    def _label_text(self):
        return "Online" if self._req_internet else "Offline"

    @property
    def req_internet(self):
        return self._req_internet

    @req_internet.setter
    def req_internet(self, value):
        self._req_internet = value
        self.req_internet_label.config(text=self._label_text())
        self.req_internet_indicator.req_internet = value

class ProviderListItem(SmartEventMixin , Frame):
    def __init__(self, parent, provider_id : str ,name : str, req_internet : bool, **kwargs):
        super().__init__(parent, bg="white", cursor="hand2", border=1, **kwargs)
        #
        self._provider_id = provider_id
        self.provider_name_lb = tk.Label(self, text=name, font=("Ubuntu", 11, "bold"), bg=self["bg"])
        self.provider_req_internet_cl = ProviderInternetReqCircle(self, req_internet, 16, bg="white")
        #
        self.config(height=25)
        self.provider_name_lb.pack(side="left", padx=(8, 0))
        self.provider_req_internet_cl.pack(side="right", padx=(0, 8))
        #
        self.bind(self.SMART_ENTER, lambda e : self.config(relief="solid"))
        self.bind(self.SMART_LEAVE, lambda e: self.config(relief="flat"))

    def _get_id(self):
        return self._provider_id

    def _set_id(self, value : str):
        self._provider_id = value

    @property
    def provider_id(self):
        return self._get_id()

    @provider_id.setter
    def provider_id(self, value : str):
        self._set_id(value)


class SelectedProviderWidget(SmartEventMixin, Frame):
    def __init__(
            self,
            master,
            provider_id : str | None = None ,
            provider_req_internet: bool = False,
            **kwargs
    ):
        super().__init__(master, **kwargs)
        #
        self._var_provider_name = StringVar(value=provider_id or "No selected")
        self._var_provider_req_internet = BooleanVar(value=provider_req_internet)
        #
        self._top_frame = Frame(self, bg=self["bg"])
        self._title_lb = Label(self._top_frame, bg=self["bg"], text="Service :", font=("Ubuntu", 14, "bold"))
        self._name_lb = Label(self._top_frame, bg=self["bg"], font=("Arial", 14), textvariable=self._var_provider_name)
        self._req_internet_widget = ProviderReqInternetWidget(self, bg=self["bg"])
        #
        self._top_frame.pack(side="top", fill="x", expand=True)
        self._req_internet_widget.pack(side="bottom", anchor="e", padx=15)
        self._title_lb.pack(side="left", fill="y", anchor="w")
        self._name_lb.pack(side="left", fill="both", expand=True, padx=8, pady=4)
        #

    @property
    def provider_name(self) -> str:
        return self._var_provider_name.get()

    @provider_name.setter
    def provider_name(self, value : str):
        self._var_provider_name.set(value)

    @property
    def provider_req_internet(self) -> bool:
        return self._req_internet_widget.req_internet

    @provider_req_internet.setter
    def provider_req_internet(self, value : bool):
        self._req_internet_widget.req_internet = value

    def display_provider(self, name : str, status : bool):
        self.provider_name = name
        self.provider_req_internet = status


class ProviderListWidget(SmartEventMixin, Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        #
        self.config(height=20, bg=master["bg"], relief="solid", border=1, padx=1, pady=1)

    def clear_provider_list(self):
        for items in self.winfo_children(): items.destroy()

    def remove_provider(self, api_id : str) :
        children : List[Widget | ProviderListItem] = self.winfo_children()
        #
        for item  in children:
            if hasattr(item, "provider_id") and item.provider_id == api_id :
                item.destroy()
                return
            #
        raise KeyError(f"No api with the id {api_id} has found")

class ProviderComboBox(SmartEventMixin, Frame):
    PROVIDER_SELECTED = "<<ProviderSelected>>"

    def __init__(self, master, values : list[tuple[str, str, bool]] | None = None, **kwargs):
        super().__init__(master, relief="solid", border=1, cursor="hand2",**kwargs)
        #
        self.provider_selected = SelectedProviderWidget(self, bg=self["bg"])
        self.float_frame = FloatFrame(self, bg=self["bg"])
        self.float_frame.attributes("-alpha", 0.0)
        self.provider_list_widget = ProviderListWidget(self.float_frame)
        #
        self._provider_data : Dict[str, Tuple[str, bool]] = {}
        self.values = values or []
        self._var_select_id = StringVar()
        #
        self.provider_selected.pack(fill="both", expand=True, pady=(0, 4), padx=1)
        self.provider_list_widget.pack(fill="both", expand=True)

        #Bind Events
        self.bind_all("<Configure>", self.update_provider_list, "+")
        self.provider_selected.bind(self.SMART_L_CLICK, self._toggle_float_menu)

    def _toggle_float_menu(self, event : Event):
        if self.provider_list_widget._is_inside(event.widget) : return
        if not self._is_inside(event.widget) :
            self.after(100, self.float_frame.hide)
        else:
            self.after(100, self.float_frame.toggle_menu)

    def set_values(self, values : list[tuple[str, str, bool]]):
        self._provider_data.clear()
        self.provider_list_widget.clear_provider_list()
        #
        for value in values :
                api_id, name, status = value
                #
                self._provider_data[api_id] = (name, status)
                #
                item = ProviderListItem(self.provider_list_widget, api_id, name, status)
                item.bind(self.SMART_L_CLICK, self._on_item_selected, "+")
                item.pack(fill="x", expand=True, anchor="n", pady=2, padx=2)

    def get_values(self):
        return [(k, v[0], v[1]) for k, v in self._provider_data.items()]

    def set(self, api_id):
        self._var_select_id.set(api_id)
        self.set_selected_provider(api_id)

    def get(self):
        return self._var_select_id.get()

    @property
    def values(self):
        return self.get_values()

    @values.setter
    def values(self, values :  list[tuple[str, str, bool]]):
        self.set_values(values)

    def _on_item_selected(self, event : Event):
        w : ProviderListItem = event.widget
        if not w or not isinstance(w, ProviderListItem): return ""
        #
        self.set_selected_provider(w.provider_id)
        self.float_frame.hide()
        #
        return "break"

    def set_selected_provider(self, provider_id : str):
        data = self._provider_data.get(provider_id)
        if not data:
            raise ValueError(f"No provider with the id {provider_id} found")
        #
        self.provider_selected.display_provider(*data)
        self.float_frame.hide()
        #
        self._var_select_id.set(provider_id)
        self.event_generate(self.PROVIDER_SELECTED)

    def update_provider_list(self, event : Event = None):
        w, h = self.winfo_width(), self.float_frame.winfo_reqheight()
        x, y = self.winfo_rootx(), self.winfo_rooty() + self.winfo_height() + 2
        self.float_frame.resize(w, h)
        self.float_frame.move_to(x, y)



if __name__ == "__main__":
    root = tk.Tk()
    root.config(background="white")
    root.geometry("500x700")
    selector = ProviderComboBox(root, width=200, height=80, values= [
        ("1", "Google", True),
        ("2", "Deepseek", True),
        ("3", "ArgosTrans", False)
    ])
    selector.bind(selector.PROVIDER_SELECTED, lambda _ : print(f"L'api {selector.get()} a ete selectionnee"))
    selector.pack(side="top")
    root.mainloop()

