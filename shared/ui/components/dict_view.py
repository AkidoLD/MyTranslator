import os.path
import tkinter

from tkinter.ttk import Frame, Label, Button, Style
from typing import Callable, List, Dict, Tuple


from shared.domain.interfaces.data_form import DataForm
from shared.domain.interfaces.form_field import FormField
from shared.infra.utils.image_utils import ImageUtils
from shared.infra.utils.validation_utils import validate_type, validate_not_empty, validate_callable
from shared.ui.components.advanced_entry import AdvancedEntry
from shared.ui.components.scroll_pane import ScrollPane



class DictViewItem(Frame, FormField):
    _DEL_IMG_PATH = os.path.join(os.path.dirname(__file__), "../../resources/icons8-minus-100-2.png")
    KEY_NAME = "key_field"
    KEY_CODE = "value_field"

    def __init__(
            self,
            master,
            key : str,
            value : str = "",
            background : str = None,
            font : str | Tuple[str, int] | Tuple[str, int, str] = None,
            readonly : bool = False,
            on_delete_btn_clicked : Callable[[str], None] = None,
            **kwargs
    ):
        Frame.__init__(self, master, style="DictViewItem.TFrame",**kwargs)
        FormField.__init__(self, key, False)
        #
        self._font = font or ("", 11, "bold")
        self._background = background or "#e5e5e5"
        self._del_img = ImageUtils.get_tk_image(self._DEL_IMG_PATH, (20, 20))
        self.on_delete_btn_clicked = on_delete_btn_clicked
        #
        self._key_label : Label | None = None
        self._value_label : Label | None = None
        self._delete_btn : Button | None = None
        #
        self._build_ui()
        self._set_style()
        self._bind_events()
        #
        self.key = key
        self.value = value
        #
        self.readonly = readonly

    def _build_ui(self):
        self._key_label = Label(self, style="Label.DictViewItem.TLabel", anchor='center', font=self._font, padding= 0)
        lang_separator = Label(self, text=":", style="Label.DictViewItem.TLabel", font=self._font)
        self._value_label = Label(self, style="Label.DictViewItem.TLabel", anchor='center', font=self._font)
        self._delete_btn = Button(self, image=self._del_img, style="DeleteBtn.DictViewItem.TButton", cursor="hand2", padding=(4, 0))
        #
        self._key_label.grid(row=0 , column=0)
        lang_separator.grid(row=0 , column=1)
        self._value_label.grid(row=0 , column=2)
        self._delete_btn.grid(row=0 , column=3)
        #
        self.grid_columnconfigure(0, weight=1, uniform='group1')
        self.grid_columnconfigure(2, weight=1, uniform='group1')

    def _set_style(self):
        self.config(padding=2)
        #
        Style().configure("DictViewItem.TFrame", background=self._background, relief="solid", borderwidth=1)
        Style().configure("Label.DictViewItem.TLabel", background=self._background)
        Style().configure('DeleteBtn.DictViewItem.TButton', relief="flat", background="#ff4c4c", font=self._font)
        Style().map(
            "DeleteBtn.DictViewItem.TButton",
                background=[
                    ("active", "#ff0f0f"),
                    ("pressed", "#c42727"),
                    ("disabled", "#f5b7b7"),
                ]
        )

    def _bind_events(self):
        self._delete_btn.configure(command=self._handler_on_delete_btn_clicked)

    def _handler_on_delete_btn_clicked(self):
        if self.on_delete_btn_clicked :
            self.on_delete_btn_clicked(self.name)

    @property
    def on_delete_btn_clicked(self):
        return self._on_delete_btn_clicked

    @on_delete_btn_clicked.setter
    def on_delete_btn_clicked(self, value):
        self._on_delete_btn_clicked = validate_callable(value, "on_delete_btn_clicked")

    @property
    def key(self):
        return self._key_label.cget('text')

    @key.setter
    def key(self, value):
        self._key_label.config(
            text=validate_not_empty(validate_type(value, str, "key"), "key").strip()
        )

    @property
    def value(self):
        return self._value_label.cget('text')
    
    @value.setter
    def value(self, value):
        self._value_label.config(
            text=validate_type(value, str, "value").strip()
        )

    def set(self, value: tuple):
        if len(validate_type(value, tuple, "value")) != 2 :
            raise RuntimeError(f"the expected value must be a tuple of 2 values, got {value}")
        #
        self.key, self.value = value

    def get(self) -> tuple :
        return self.key, self.value

    def _enable(self):
        self._delete_btn.configure(state='normal')

    def _disable(self):
        self._delete_btn.configure(state='disabled')

    def reset(self):
        pass

class DictView(Frame, DataForm, FormField):
    _ADD_IMG_PATH = os.path.join(os.path.dirname(__file__), "../../resources/icons8-add-new-100.png")

    def __init__(
            self,
            master,
            title : str,
            name : str = "dict_view",
            key_name : str = "key",
            value_name : str = "value",
            font : Tuple[str, int] | Tuple[str, int, str] = None,
            required: bool = False,
            inside_color : str = 'white',
            outline_color : str = 'light gray',
            allow_empty_value : bool = False,
            allow_repeated_value: bool = False,
            on_changed : Callable[[int], None] = None,
            **kwargs
    ):
        Frame.__init__(self, master, **kwargs)
        FormField.__init__(self, name, required, on_changed=on_changed)
        DataForm.__init__(self)
        #
        self._key_name = key_name
        self._value_name = value_name
        self._font = font or ("Ubuntu", 13)
        #
        self._allow_empty_value = allow_empty_value
        self._allow_repeated_value = allow_repeated_value
        #
        self._inside_color = inside_color
        self._outline_color = outline_color
        #
        self._add_img = ImageUtils.get_tk_image(self._ADD_IMG_PATH, (22, 22))
        #
        self._build_ui()
        self._set_style()
        self._bind_events()
        #
        self.title = title
        #
        self._check_fields()

    def _build_ui(self):
        title_pane = Frame(self, style="TitlePane.DictView.TFrame")
        self._title_lb = Label(
            title_pane,
            style='Label.DictView.TLabel',
            font=(self._font[0], self._font[1] + 1, 'bold')
        )
        #
        self._item_count_lb = Label(
            title_pane,
            style='Label.DictView.TLabel',
            font=(self._font[0], self._font[1] + 1, 'bold'),
            text="(0)"
        )
        #
        content_scroll = ScrollPane(self)
        self._content_pane = content_scroll.pane
        self._content_pane.config(height=50, padx=2, pady=2, background=self._inside_color)
        #
        self._add_value_pane = Frame(self, style='AddValuePane.DictView.TFrame')
        _entry_pane = Frame(self._add_value_pane, padding=2, style='AddValuePane.DictView.TFrame')
        self._key_entry = AdvancedEntry(_entry_pane, placeholder=self._key_name, font=self._font,
                                        style="Entry.DictView.TEntry", width=0)
        self._value_entry = AdvancedEntry(_entry_pane, placeholder=self._value_name, font=self._font,
                                          style="Entry.DictView.TEntry", width=0)
        #
        separator = Label(_entry_pane, text=":", style='Label.DictView.TLabel', font=("", 12, 'bold'))
        self._add_value_btn = Button(self._add_value_pane, image=self._add_img,
                                     style="AddBtn.DictView.TButton")


        #
        title_pane.pack(side='top', fill='x')
        self._title_lb.pack(side='left', padx=3)
        self._item_count_lb.pack(side='left', padx=2)
        #
        content_scroll.pack(fill='both', expand=True, padx=2, pady=(2, 0))
        #
        self._add_value_pane.pack(side='bottom', fill='x')
        _entry_pane.pack(side='left', fill='both', expand=True)
        self._key_entry.pack(side='left', expand=True, fill='both')
        separator.pack(side='left', padx=4)
        self._value_entry.pack(side='left', expand=True, fill='both')
        self._add_value_btn.pack(side='right', fill='x')

    def _set_style(self):
        self._add_value_pane.configure(padding=1)
        self._add_value_btn.configure(cursor="hand2")
        #
        Style().configure(
            "TitlePane.DictView.TFrame",
            background=self._outline_color
        )
        #
        Style(self).configure('Entry.DictView.TEntry', padding=(5, 0), fieldbackground="white")
        Style(self).map(
            'Entry.DictView.TEntry',
            fieldbackground=[
                ("disabled", "light gray"),
                ("readonly", "light gray")
            ]
        )
        #
        Style(self).configure("Label.DictView.TLabel", background=self._outline_color)
        #
        Style(self).configure('AddBtn.DictView.TButton', background="#e9e9ff", padding=(10, 0), relief="raised")

        Style(self).map('AddBtn.DictView.TButton',
                        background=[('active', "#d2d0ff"), ("pressed", "#9195d4"), ("disabled", "#a8a8a8")])
        Style().configure(
            'AddValuePane.DictView.TFrame',
            background=self._outline_color
        )

    def _bind_events(self):
        self._key_entry.bind(AdvancedEntry.TEXT_CHANGED, lambda e: self._check_fields(), "+")
        self._value_entry.bind(AdvancedEntry.TEXT_CHANGED, lambda e: self._check_fields(), "+")
        #
        self._value_entry.bind("<FocusIn>", lambda e: self._check_fields(), "+")
        self._key_entry.bind('<FocusIn>', lambda e: self._check_fields(), "+")
        #
        self._add_value_btn.configure(command=self._on_add_value_btn_clicked)

    def _handler_on_changed(self):
        self._item_count_lb.configure(text=f"({len(self.get())})")
        super()._handler_on_changed()

    def _add_item(self, key: str, value: str):
        lang_widget = DictViewItem(self._content_pane, key, value, on_delete_btn_clicked=self._remove_item, readonly=self.readonly)
        lang_widget.pack(side='top', fill='x', pady=2)
        self._check_fields()
        self._handler_on_changed()

    def _remove_item(self, key: str):
        w = self._get_item(key)
        if not w: return
        w.destroy()
        self._handler_on_changed()

    def _clear_items(self):
        for i in self._get_items(): i.destroy()
        self._handler_on_changed()

    def _check_fields(self) -> bool:
        key = self._key_entry.get()
        value = self._value_entry.get()
        #
        is_valid = True
        #Check key
        if not key.strip() or key in self.get().keys(): is_valid = False
        #Check value
        if ((not self._allow_empty_value and not value.strip()) or
                (not self._allow_repeated_value and value in self.get().values())): is_valid = False
        #
        self._add_value_btn.configure(state='normal' if is_valid else 'disabled')
        #
        return is_valid

    def _get_item(self, key : str):
        for w in self._content_pane.winfo_children():
            if isinstance(w, DictViewItem) and w.key == key :
                return w
        print(f"No ProviderLangWidget with the name {key} found")
        return None

    def _get_items(self) -> List[DictViewItem]:
        return [w for w in self._content_pane.winfo_children() if isinstance(w, DictViewItem)]

    def get_item_count(self):
        return len(self._get_items())

    #----- Events ---------------------------------------------------------------------
    def _on_add_value_btn_clicked(self):
        if not self._check_fields(): return
        #
        lang_name = self._key_entry.get().strip()
        lang_code = self._value_entry.get().strip()
        #
        self._add_item(lang_name, lang_code)
        #
        self._value_entry.text = ""
        self._key_entry.text = ""
        #
        self._check_fields()

    @property
    def title(self):
        return self._title_lb.cget('text')

    @title.setter
    def title(self, value):
        self._title_lb.configure(text=validate_not_empty(validate_type(value, str, "title"), "title"))

    #----- FormField Methods -----------------------------------------------------------
    def set(self, value: Dict[str, str]):
        self.reset()
        for key, value in value.items() : self._add_item(key, value)

    def get(self) -> Dict[str, str]:
        return {w.key : w.value for w in self._get_items()}

    def _enable(self):
        self._add_value_btn.configure(state="normal")
        self._key_entry.configure(state="normal")
        self._value_entry.configure(state="normal")
        #
        self._check_fields()
        for child in self._get_items(): child.readonly = False

    def _disable(self):
        self._add_value_btn.configure(state="disabled")
        self._key_entry.configure(state="readonly")
        self._value_entry.configure(state="readonly")
        #
        self._check_fields()
        for child in self._get_items(): child.readonly = True

    @property
    def readonly(self) -> bool:
        return self._readonly

    @readonly.setter
    def readonly(self, value : bool):
        if value == self._readonly : return
        #
        self._readonly = value
        self._disable() if value else self._enable()

    def reset(self):
        self._clear_items()


if __name__ == "__main__":
    root = tkinter.Tk()
    root.geometry("500x400")
    Style().theme_use("clam")
    widget = DictView(root, "Langues", key_name="Nom", value_name="Code", allow_repeated_value=True)
    widget.readonly = True
    widget.set({"Francais": "fr", "Anglais": "en"})
    widget.on_changed = lambda v : print(v)
    widget.pack(fill='both', expand=True)
    root.mainloop()