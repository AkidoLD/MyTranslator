import os.path
import tkinter
import uuid

from tkinter import Widget, Frame
from tkinter.ttk import Button, Style
from typing import Dict, Self, Tuple, Callable, Type

from shared.infra.utils.image_utils import ImageUtils
from shared.infra.utils.validation_utils import validate_type, validate_not_empty, validate_callable
from shared.ui.components.stack_frame import StackFrame


class MenuStackButton(Frame):
    _PLUS_IMG_PATH = os.path.join(os.path.dirname(__file__), "../../resources/icons8-plus-math-100.png")
    _MINUS_IMG_PATH = os.path.join(os.path.dirname(__file__), "../../resources/icons8-minus-100-4.png")
    _IMG_SIZE = (20, 20)
    #
    _EMPTY_STYLE = "Empty.MenuStackButton.TButton"
    _NOT_EMPTY_STYLE = "NoEmpty.MenuStackButton.TButton"
    #
    def __init__(
            self,
            master,
            menu_id,
            text : str,
            group_id : str = None,
            font : Tuple[str] | Tuple[str, int] | Tuple[str, int, str] = ("", 12, "bold"),
            command : Callable[[str], None] = None,
            **kwargs
    ):
        super().__init__(master, **kwargs)
        #
        self.id = menu_id
        self.group_id = group_id
        self.command = command
        self._is_dropped = False
        #
        self._plus_img = ImageUtils.get_tk_image(self._PLUS_IMG_PATH, self._IMG_SIZE)
        self._minus_img = ImageUtils.get_tk_image(self._MINUS_IMG_PATH, self._IMG_SIZE)
        #
        Style().configure(
            self._EMPTY_STYLE,
            background="white",
            font=font
        )
        Style().map(
            self._EMPTY_STYLE,
            background=[
                ("active", "#eeeeee"),
                ("disabled", "#636363"),
            ]
        )
        #
        Style().configure(
            self._NOT_EMPTY_STYLE,
            background="#c6c6c6",
            font=font
        )
        #
        Style().map(
            self._NOT_EMPTY_STYLE,
            background=[
                ("active", "#8d8d8d"),
                ("disabled", "#636363"),
            ]
        )
        #
        self._menu_btn = Button(self, style=self._EMPTY_STYLE, cursor="hand2", command=self._handle_command, padding=0)
        self._toggle_btn = Button(self, image=self._plus_img, command=self._toggle_items, style=self._NOT_EMPTY_STYLE, cursor="hand2", padding=0)
        self._items_pane = Frame(self)
        #
        self.text = text
        #
        self._menu_btn.grid(row=0, column=0, sticky='nsew')

        #
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

    def _handle_command(self):
        if self.command :
            self.command(self.id)

    def _toggle_items(self):
        self._is_dropped = not self._is_dropped
        #
        if self._is_dropped :
            self._toggle_btn.configure(image=self._minus_img)
            self._show_items()
        else :
            self._toggle_btn.configure(image=self._plus_img)
            self._hide_items()

    def _item_count(self) -> int:
        return len(self._items_pane.winfo_children())

    def _show_toggle_btn(self):
        self._toggle_btn.grid(row=0, column=1, sticky="nswe")

    def _hide_toggle_btn(self):
        self._toggle_btn.grid_forget()

    def _show_items(self):
        self._items_pane.grid(row=1, column=0, columnspan=2, sticky="nswe")

    def _hide_items(self):
        self._items_pane.grid_forget()

    def _get_item(self, item_id):
        for i in self._items_pane.winfo_children() :
            if isinstance(i, MenuStackButton) and i.id == item_id :
                return i
        return None

    def add_item(self, item_id, text : str, **kwargs) -> Self:
        item = MenuStackButton(self._items_pane, item_id, text, group_id=self.id, **kwargs)
        item.pack(side='top', fill='x', expand=True, pady=1, padx=0)
        if self._item_count() == 1 :
            self._menu_btn.config(style=self._NOT_EMPTY_STYLE)
            self._show_toggle_btn()
        return item

    def remove_item(self, item_id):
        item = self._get_item(item_id)
        if not item :
            raise ValueError(f"No item found with id {item_id}")
        #
        item.destroy()
        if not self._item_count() :
            self._hide_toggle_btn()
            self._menu_btn.config(style=self._EMPTY_STYLE)
            self._hide_items()

    #--- Properties ---------------------------------------------------------------
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value : str):
        self._id = validate_not_empty(validate_type(value, str, "id"), "id")

    @property
    def text(self):
        return self._menu_btn.cget('text')

    @text.setter
    def text(self, value : str):
        self._menu_btn.config(text=validate_not_empty(validate_type(value, str, "text"), "text"))

    @property
    def group_id(self) -> str | None :
        return self._group_id

    @group_id.setter
    def group_id(self, value : str):
        self._group_id = None if value is None else validate_not_empty(value, "group_id")
        
    @property
    def command(self):
        return self._command
    
    @command.setter
    def command(self, value):
        self._command = validate_callable(value, "command")


class MenuStack(Frame):
    def __init__(
            self,
            master,
            **kwargs
    ):
        super().__init__(master, **kwargs)
        #
        self._menu_buttons : Dict[str, MenuStackButton]= {}
        #
        self._btn_pane = Frame(self, width=180, padx=2, pady=2, relief='groove', bd=1)
        self._btn_pane.pack_propagate(False)
        #
        self._content_stack = StackFrame(self)
        #
        self._btn_pane.pack(side='left', fill='y')
        self._content_stack.pack(fill='both', expand=True)

    def _add_menu_btn(self, text : str, menu_id : str, group_id : str = None):
        if menu_id in self._menu_buttons.keys():
            raise ValueError(f"menu_id {menu_id} already exist")
        #
        master = self._btn_pane if group_id is None else self._menu_buttons.get(validate_type(group_id, str, "group_id"))
        if not master :
            raise ValueError(f"no menu button found with id {group_id}.")
        #
        _btn = None

        if isinstance(master, MenuStackButton) :
            _btn = master.add_item(menu_id, text)
        else:
            _btn = MenuStackButton(master, menu_id, text, group_id)
            _btn.pack(side="top",fill='x', pady=1)
        #
        self._menu_buttons[menu_id] = _btn
        #
        return _btn

    def add_menu(self, title : str, menu_class : Type[Widget] = None, menu_id : str = None,  group_id : str = None, **kwargs):
        if menu_class and not issubclass(menu_class, Widget):
            raise TypeError(f"menu_class must be subclass of Widget, got class {type(menu_class)}")
        #
        menu_id = menu_id or str(uuid.uuid4())
        _btn = self._add_menu_btn(title, menu_id, group_id)
        #
        if menu_class :
            _btn.command = self._content_stack.raise_item
            return self._content_stack.add_item(menu_id, menu_class, **kwargs)
        #
        return None


if __name__ == "__main__" :
    root = tkinter.Tk()
    root.geometry("500x400")
    #
    pane = MenuStack(root)
    app_frame = pane.add_menu("Application", tkinter.Frame, "application", background="yellow")
    config_pane = pane.add_menu("Configuration", tkinter.Frame,"config", "application", background="pink")
    lang_setting = pane.add_menu("Languages", tkinter.Frame, "config", background="cyan")
    #
    Button(app_frame, text="App frame btn").pack(side='top', fill='x')
    Button(config_pane, text="Config frame btn").pack(side='top', fill='x')
    Button(lang_setting, text="Language frame btn").pack(side='top', fill='x')
    #color
    pane.pack(fill='both', expand=True)
    root.mainloop()
