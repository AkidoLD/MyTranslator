import tkinter as tk
from tkinter import Label, Frame, Event
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
        self._status = status

        self.status_label = Label(self, bg=self["bg"],text=self._label_text(), font=("Ubuntu", 11))
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
    API_SELECTED = "<<ApiSelected>>"
    """Signal emmit when a Api is selected"""
    def __init__(self, parent, _id : str ,name : str, status : bool, **kwargs):
        super().__init__(parent, bg="white", cursor="hand2", border=1, **kwargs)
        self.api_id = _id
        self.api_name = tk.Label(self, text=name, font=("Ubuntu", 10, "bold"), bg=self["bg"])
        self.api_status = ApiStatusCircle(self, 20, status, bg="white")
        #
        self.api_name.pack(side="left", padx=(8, 0))
        self.api_status.pack(side="right", padx=(0, 8))
        self.config(height=20)
        #
        self.bind(self.SMART_L_CLICK, self.on_clicked)
        self.bind(self.SMART_ENTER, lambda e : self.config(relief="solid"))
        self.bind(self.SMART_LEAVE, lambda e: self.config(relief="flat"))

    def on_clicked(self, event : Event = None):
        self.event_generate(self.API_SELECTED)

    def get_data(self) -> dict:
        return {"_id" : self.api_id, "name" : self.api_name.cget("text"), "status" : self.api_status.status}

class ApiSelected(SmartEventMixin, Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        #
        self.api_select_id = None
        self.api_selected_top_frame = Frame(self)
        self.api_selected_status = ApiStatusWidget(self, bg=self["bg"])
        self.api_selected_title = Label(self.api_selected_top_frame,bg=self["bg"], text="services :", font=("Ubuntu", 14, "bold"))
        self.api_selected_name = Label(self.api_selected_top_frame, bg=self["bg"], text="No selected", font=("Ubuntu", 12))
        #
        self.api_selected_top_frame.pack(side="top", fill="x", expand=True)
        self.api_selected_status.pack(side="bottom", anchor="e")
        self.api_selected_title.pack(side="left", fill="y", anchor="w")
        self.api_selected_name.pack(side="left", fill="both", expand=True)

    def set_selected_api(self, _id : str, name : str, status : bool):
        self.api_select_id = _id
        self.api_selected_name.config(text=name)
        self.api_selected_status.status = status

class ApiList(SmartEventMixin, Frame):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.config(height=20, bg=master["bg"], relief="solid", border=1)

    def add_api(self, _id : str, name : str, status : bool) -> ApiListItem:
        item = ApiListItem(self, _id, name, status)
        item.pack(side="top", pady=2, padx=2, fill="x", expand=True)
        return item

    def remove_api(self, _id : str) -> ApiListItem | None:
        for item in self.winfo_children():
            if hasattr(item, "api_id") and item.api_id == _id :
                item.pack_forget()
                return item
        return None


class ApiComboBox(SmartEventMixin, Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, relief="solid", border=1, **kwargs)
        self.api_selected = ApiSelected(self, bg=self["bg"])
        self.float_frame = FloatFrame(self, bg=self["bg"])
        self.float_frame.attributes("-alpha", 0.0)
        self.api_list = ApiList(self.float_frame)
        self.pack_propagate(False)
        #
        self.api_selected.pack(fill="both", expand=True, pady=1, padx=1)
        self.api_list.pack(fill="both", expand=True)

        #Api test
        self.add_api("google", "Google", True)
        self.add_api("trans", "TranslateService", False)
        self.add_api("arg_trans", "Argos TranslateService", True)

        #Bind Events
        self.api_selected.bind(SmartEventMixin.SMART_L_CLICK, self.on_api_selected_clicked, "+")
        self.bind_all("<Configure>", self.update_api_list)

    def add_api(self, _id : str, name : str, status : bool):
        item = self.api_list.add_api(_id, name, status)
        item.bind(ApiListItem.API_SELECTED, self.on_api_selected, "+")
        item.bind(ApiListItem.API_SELECTED, lambda e : self.float_frame.hide(), "+")


    def on_api_selected_clicked(self, event : Event = None):
        self.float_frame.toggle_menu()
        self.update_api_list()

    def on_api_selected(self, event : Event):
        data = event.widget.get_data()
        print(f"Api selected {data}")
        self.api_selected.set_selected_api(**data)

    def update_api_list(self, event : Event = None):
        w, h = self.winfo_width(), self.float_frame.winfo_reqheight()
        x, y = self.winfo_rootx(), self.winfo_rooty() + self.winfo_height() + 5
        self.float_frame.resize(w, h)
        self.float_frame.move_to(x, y)



if __name__ == "__main__":
    root = tk.Tk()
    root.config(background="white")
    root.geometry("500x700")
    selector = ApiComboBox(root, width=200, height=80)
    selector.pack_propagate(False)
    selector.pack(side="top")
    root.mainloop()

