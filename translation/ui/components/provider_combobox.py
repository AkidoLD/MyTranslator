import tkinter
from tkinter import Event
from tkinter.ttk import Frame, Label, Style, Button
from typing import Tuple, Iterable


from shared.infra.utils.validation_utils import validate_type, validate_not_empty
from shared.ui.components.smart_frame import SmartFrame
from translation.ui.components.provider_combobox_item import ProviderComboboxItem, ProviderInternetReqCircle


class ProviderCombobox(Frame):
    PROVIDER_SELECTED = "<<ProviderSelection>>"
    #
    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            padding=0,
            **kwargs
        )
        #
        _bg_color = '#868686'
        _h_color = '#a2a2a2'
        #

        _content_pane = SmartFrame(
            self,
            padding=3,
            cursor="hand2",
            style="ContentFrame.ProviderCombobox.TFrame"
        )
        #
        title_lb = Label(
            _content_pane,
            text="Service : ",
            anchor='center',
            style="TitleLabel.ProviderCombobox.TLabel",
            font=("Arial", 13, "bold")
        )
        self._provider_name_lb = Label(
            _content_pane,
            text="No Selected",
            anchor='center',
            style="ProviderName.ProviderCombobox.TLabel",
            font = ("Ubuntu", 14)
        )
        self._provider_req_internet_lb = Label(
            _content_pane,
            style="ReqInternetLabel.ProviderCombobox.TLabel",
            font=("Ubuntu", 11, "bold")
        )
        self._provider_req_internet_cl = ProviderInternetReqCircle(
            _content_pane,
            None,
            diameter=15,
            color="#f7f7f7",
            width=1,
            background=_bg_color
        )
        #
        self._item_frame= Frame(self.winfo_toplevel(), style="ItemFrame.ProviderCombobox.TFrame", padding=1)
        #
        self.req_internet = None
        self.name = "No Selected"
        self.p_id = None
        #
        #
        _content_pane.pack(fill="both", expand=True)
        #
        title_lb.grid(row=0, column=0, sticky='nswe', padx=2)
        self._provider_name_lb.grid(row=0, column=1, columnspan=3, sticky='nswe', padx=4, pady=8)
        self._provider_req_internet_lb.grid(row=1, column=2, padx=1)
        self._provider_req_internet_cl.grid(row=1, column=3, padx=1)
        #
        _content_pane.grid_columnconfigure(1, weight=1)
        _content_pane.grid_rowconfigure(0, weight=1)
        #
        style = Style()
        #
        style.configure("ContentFrame.ProviderCombobox.TFrame", background=_bg_color, borderwidth=1, relief='solid')
        style.map("ContentFrame.ProviderCombobox.TFrame", background=[('active', _h_color)])

        style.configure("TitleLabel.ProviderCombobox.TLabel", background=_bg_color)
        style.map("TitleLabel.ProviderCombobox.TLabel", background=[('active', _h_color)])

        style.configure("ProviderName.ProviderCombobox.TLabel", background=_bg_color)
        style.map("ProviderName.ProviderCombobox.TLabel", background=[('active', _h_color)])

        style.configure("ReqInternetLabel.ProviderCombobox.TLabel", background=_bg_color)
        style.map("ReqInternetLabel.ProviderCombobox.TLabel", background=[('active', _h_color)])

        style.configure("ItemFrame.ProviderCombobox.TFrame", background="#e1e1e1", borderwidth=1, relief='solid')

        def _on_enter(_):
            title_lb.state(["active"])
            self._provider_name_lb.state(["active"])
            self._provider_req_internet_lb.state(["active"])
            self._provider_req_internet_cl.configure(background=_h_color)
            _content_pane.state(["active"])

        def _on_leave(_):
            title_lb.state(["!active"])
            self._provider_name_lb.state(["!active"])
            self._provider_req_internet_lb.state(["!active"])
            self._provider_req_internet_cl.configure(background=_bg_color)
            _content_pane.state(["!active"])

        _content_pane.bind(_content_pane.SMART_ENTER, _on_enter)
        _content_pane.bind(_content_pane.SMART_LEAVE, _on_leave)
        #
        _content_pane.bind(SmartFrame.SMART_L_CLICK, lambda  _ : self._toggle_item_frame())
        self._item_frame.bind("<FocusOut>", lambda _ : self._hide_item_frame())

    def _show_item_frame(self):
        self._item_frame.place(in_=self, relwidth=1.0, relx=0, rely=1.02)
        self._item_frame.lift()
        self._item_frame.focus_force()

    def _hide_item_frame(self):
        self._item_frame.place_forget()

    def _toggle_item_frame(self):
        self._hide_item_frame() if self._item_frame.winfo_ismapped() else self._show_item_frame()

    @property
    def name(self):
        return self._provider_name_lb.cget('text')

    @name.setter
    def name(self, value : str):
        if value is None:
            self._name = None
        else:
            self._name = validate_not_empty(validate_type(value, str, "name"), "name")
            #
        self._provider_name_lb.config(text=value or "No Selected")

    @property
    def req_internet(self):
        return self._provider_req_internet_cl.req_internet

    @req_internet.setter
    def req_internet(self, value):
        self._provider_req_internet_cl.req_internet = value
        text = "" if value is None else "Online" if value else "Offline"
        self._provider_req_internet_lb.config(text=text)


    @property
    def p_id(self):
        return self._p_id

    @p_id.setter
    def p_id(self, value):
        if value is None:
            self._p_id = None
        else:
            self._p_id = validate_not_empty(validate_type(value, str, "provider_id"), "provider_id")

    def set(self, value : Tuple[str, str, bool] | None):
        self.p_id, self.name, self.req_internet = value or (None, None, None)
        self.event_generate(self.PROVIDER_SELECTED)

    def get(self) -> Tuple[str, str, bool]:
        return self.p_id, self.name, self.req_internet

    def clear_items(self):
        for c in self._item_frame.winfo_children(): c.destroy()

    def set_values(self, values : Iterable[Tuple[str, str, bool]]):
        self.clear_items()
        for t in values :
            p = ProviderComboboxItem(self._item_frame, *t)
            p.bind(p.SMART_L_CLICK, self._on_item_selected)
            p.pack(side='top', fill='x')

    @property
    def values(self):
        return [(item.p_id, item.name, item.req_internet) for item in self._item_frame.winfo_children()]

    @values.setter
    def values(self, value):
        self.set_values(value)

    def _on_item_selected(self, e : Event):
        self.set(e.widget.get())
        self._hide_item_frame()


if __name__ == "__main__":
    root = tkinter.Tk()
    root.config(background="white")
    root.geometry("500x700")
    #
    combo = ProviderCombobox(root)
    combo.set_values([("1", "Google", True), ("2", "Translate", False)])
    combo.pack(side='top')
    Button(root, text="Test Focus").pack(side='top', fill='x')
    print(combo.get())
    root.mainloop()
