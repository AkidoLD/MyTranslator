import tkinter as tk

from tkinter import Label, Frame, Event, StringVar, BooleanVar, Widget
from typing import List, Tuple, Dict

from shared.ui.components.circle_widget import CircleWidget
from shared.ui.components.float_menu import FloatFrame
from shared.ui.mixins.smart_events import SmartEventMixin


class ApiStatusCircle(CircleWidget):
    def __init__(self, parent, diameter : float, status : bool = False, **kwargs):
        super().__init__(parent, diameter, outline="", **kwargs)
        self.status = status

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value
        self.color = "green" if self._status else "blue"

class ApiStatusWidget(tk.Frame):
    def __init__(self, parent, status=False, **kwargs):
        super().__init__(parent, **kwargs)
        #
        self._status = status
        self.status_label = Label(self, bg=self["bg"],text=self._label_text(), font=("Ubuntu", 11, "bold"))
        self.status_indicator = ApiStatusCircle(self, 15, status, bg=self["bg"])

        self.status_label.pack(side="left")
        self.status_indicator.pack(side="left", padx=2)

    def _label_text(self):
        return "Online" if self._status else "Offline"

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value
        self.status_label.config(text=self._label_text())
        self.status_indicator.status = value

class ApiListItem(SmartEventMixin , Frame):
    def __init__(self, parent, api_id : str ,name : str, status : bool, **kwargs):
        super().__init__(parent, bg="white", cursor="hand2", border=1, **kwargs)
        #
        self._api_id = api_id
        self.api_name = tk.Label(self, text=name, font=("Ubuntu", 11, "bold"), bg=self["bg"])
        self.api_status = ApiStatusCircle(self, 16, status, bg="white")
        #
        self.api_name.pack(side="left", padx=(8, 0))
        self.api_status.pack(side="right", padx=(0, 8))
        self.config(height=25)
        #
        self.bind(self.SMART_ENTER, lambda e : self.config(relief="solid"))
        self.bind(self.SMART_LEAVE, lambda e: self.config(relief="flat"))

    def _get_id(self):
        return self._api_id

    def _set_id(self, value : str):
        self._api_id = value

    @property
    def api_id(self):
        return self._get_id()

    @api_id.setter
    def api_id(self, value : str):
        self._set_id(value)


class ApiSelectedWidget(SmartEventMixin, Frame):
    def __init__(self, master, api_name : str | None = None , api_status : bool = False, **kwargs):
        super().__init__(master, **kwargs)
        #
        self._var_api_name = StringVar(value=api_name or "No selected")
        self._var_api_status = BooleanVar(value=api_status)
        #
        self._top_frame = Frame(self, bg=self["bg"])
        self._title = Label(self._top_frame, bg=self["bg"], text="Service :", font=("Ubuntu", 14, "bold"))
        self._name = Label(self._top_frame, bg=self["bg"], font=("Arial", 14), textvariable=self._var_api_name)
        self._status = ApiStatusWidget(self, bg=self["bg"])
        #
        self._top_frame.pack(side="top", fill="x", expand=True)
        self._status.pack(side="bottom", anchor="e", padx=15)
        self._title.pack(side="left", fill="y", anchor="w")
        self._name.pack(side="left", fill="both", expand=True, padx=8, pady=4)
        #

    @property
    def api_name(self) -> str:
        return self._var_api_name.get()

    @api_name.setter
    def api_name(self, value : str):
        self._var_api_name.set(value)

    @property
    def api_status(self) -> bool:
        return self._status.status

    @api_status.setter
    def api_status(self, value : bool):
        self._status.status = value

    def display_api(self, name : str, status : bool):
        self.api_name = name
        self.api_status = status


class ApiListWidget(SmartEventMixin, Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        #
        self.config(height=20, bg=master["bg"], relief="solid", border=1, padx=1, pady=1)

    def clear_api_list(self):
        for items in self.winfo_children(): items.destroy()

    def remove_api(self, api_id : str) :
        children : List[Widget | ApiListItem] = self.winfo_children()
        #
        for item  in children:
            if hasattr(item, "api_id") and item.api_id == api_id :
                item.destroy()
                return
            #
        raise KeyError(f"No api with the id {api_id} has found")

class ApiComboBox(SmartEventMixin, Frame):
    API_SELECTED = "<<ApiSelect>>"

    def __init__(self, master, values : list[tuple[str, str, bool]] | None = None, **kwargs):
        super().__init__(master, relief="solid", border=1, cursor="hand2",**kwargs)
        #
        self.api_selected = ApiSelectedWidget(self, bg=self["bg"])
        self.float_frame = FloatFrame(self, bg=self["bg"])
        self.float_frame.attributes("-alpha", 0.0)
        self.api_list_widget = ApiListWidget(self.float_frame)
        #
        self._api_data : Dict[str, Tuple[str, bool]] = {}
        self.values = values or []
        self._var_select_id = StringVar()
        #
        self.api_selected.pack(fill="both", expand=True, pady=(0, 4), padx=1)
        self.api_list_widget.pack(fill="both", expand=True)

        #Bind Events
        self.bind_all("<Configure>", self.update_api_list, "+")
        self.api_selected.bind(self.SMART_L_CLICK, self._toggle_float_menu)

    def _toggle_float_menu(self, event : Event):
        if self.api_list_widget._is_inside(event.widget) : return
        if not self._is_inside(event.widget) :
            self.after(100, self.float_frame.hide, )
        else:
            self.after(100, self.float_frame.toggle_menu, )

    def set_values(self, values : list[tuple[str, str, bool]]):
        self._api_data.clear()
        self.api_list_widget.clear_api_list()
        #
        for value in values :
                api_id, name, status = value
                #
                self._api_data[api_id] = (name, status)
                #
                item = ApiListItem(self.api_list_widget, api_id, name, status)
                item.bind(self.SMART_L_CLICK, self._on_item_selected, "+")
                item.pack(fill="x", expand=True, anchor="n", pady=2, padx=2)

    def set(self, api_id):
        self._var_select_id.set(api_id)
        self.set_selected_api(api_id)

    def get(self):
        return self._var_select_id.get()

    @property
    def values(self):
        raise AttributeError('Values is a write-only property')

    @values.setter
    def values(self, values :  list[tuple[str, str, bool]]):
        self.set_values(values)

    def _on_item_selected(self, event : Event):
        w : ApiListItem = event.widget
        if not w or not isinstance(w, ApiListItem): return
        #
        self.set_selected_api(w.api_id)

    def set_selected_api(self, api_id : str):
        data = self._api_data.get(api_id)
        if not data:
            raise ValueError(f"No api with the id {api_id} found")
        #
        self.api_selected.display_api(*data)
        self.float_frame.hide()
        #
        self._var_select_id.set(api_id)
        self.event_generate(self.API_SELECTED)

    def update_api_list(self, event : Event = None):
        w, h = self.winfo_width(), self.float_frame.winfo_reqheight()
        x, y = self.winfo_rootx(), self.winfo_rooty() + self.winfo_height() + 2
        self.float_frame.resize(w, h)
        self.float_frame.move_to(x, y)



if __name__ == "__main__":
    root = tk.Tk()
    root.config(background="white")
    root.geometry("500x700")
    selector = ApiComboBox(root, width=200, height=80, values= [
        ("1", "Google", True),
        ("2", "Deepseek", True),
        ("3", "ArgosTrans", False)
    ])
    selector.bind(selector.API_SELECTED, lambda _ : print(f"L'api {selector.get()} a ete selectionnee"))
    selector.pack(side="top")
    root.mainloop()

