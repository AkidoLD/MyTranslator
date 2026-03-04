import os.path
from abc import ABC
from tkinter.ttk import Frame, Button, Label, Style
from tkinter import Tk, filedialog, StringVar
from typing import Tuple

from shared.domain.interfaces.data_form import DataForm
from shared.domain.interfaces.form_field import FormField
from shared.infra.utils.image_utils import ImageUtils
from shared.ui.components.dict_view import DictView
from shared.ui.components.form_field_widgets import EntryField


class ProviderAdvancedDataForm(Frame, DataForm, FormField, ABC):
    def __init__(
            self,
            master,
            name,
            readonly : bool = False,
            required : bool = True,
            **kwargs
    ):
        Frame.__init__(self, master, **kwargs)
        DataForm.__init__(self, readonly)
        FormField.__init__(self, name, required)
        #
        self.on_changed = self.on_field_changed

class ExecProviderAdvancedDataForm(ProviderAdvancedDataForm):
    PROVIDER_BINARY_FIELD = "provider_binary"
    PROVIDER_LANG_TEMPLATE_FIELD = "provider_lang_template"
    PROVIDER_ARGS_FIELD = "provider_args"
    #
    _FOLDER_IMG_PATH = os.path.join(os.path.dirname(__file__), "../../resources/icons8-folder-100-2.png")

    def __init__(
            self,
            master,
            name,
            font : Tuple[str, int] | Tuple[str, int, str] = ("", 12),
            readonly : bool = False,
            required : bool = True,
            **kwargs
    ):
        super().__init__(master, name, readonly, required, **kwargs)
        #
        self._font = font
        self._binary_path = StringVar(self, "")
        self._folder_img = ImageUtils.get_tk_image(self._FOLDER_IMG_PATH, 22)
        #
        self._build_ui()
        self._set_style()
        self._bind_events()
        #
        self.read_only(True if readonly else False)

    def _build_ui(self):
        self._provider_binary_entry = EntryField(
            self,
            self.PROVIDER_BINARY_FIELD,
            placeholder="Emplacement du binaire",
            font=self._font,
            style="Entry.ExecProviderAdvancedDataForm.TEntry",
        )
        #
        self._retrieve_binary_btn = Button(
            self,
            image=self._folder_img,
            padding=0,
            style="Button.ExecProviderAdvancedDataForm.TButton",
            cursor="hand2"
        )
        #
        self._provider_lang_template_entry = EntryField(
            self,
            self.PROVIDER_LANG_TEMPLATE_FIELD,
            placeholder="Ex : @src_lang:@target_lang",
            font=self._font,
            style="Entry.ExecProviderAdvancedDataForm.TEntry"
        )
        #
        self._args_count_lb = Label(self, text="(0)", style="TitleLabel.ExecProviderAdvancedDataForm.TLabel")
        self._provider_args_field = DictView(
            self,
            self.PROVIDER_ARGS_FIELD,
            key_name="Argument",
            value_name="Valeur",
            font=self._font,
            allow_empty_value=True,
            allow_repeated_value=True
        )
        #
        Label(
            self,
            text="Emplacement",
            style="TitleLabel.ExecProviderAdvancedDataForm.TLabel"
        ).grid(row=0, column=0, columnspan=2, sticky='nsw', pady=(1, 4))
        #
        self._provider_binary_entry.grid(row=1, column=0, sticky='nswe')
        self._retrieve_binary_btn.grid(row=1, column=1, sticky="nswe", padx=2)

        #
        Label(
            self,
            text="Template de langue",
            style="TitleLabel.ExecProviderAdvancedDataForm.TLabel"
        ).grid(row=2, column=0, columnspan=2, sticky='nsw', pady=(50, 5))
        self._provider_lang_template_entry.grid(row=3, column=0, columnspan=2, sticky='nswe')

        #
        Label(
            self,
            text="Arguments",
            style="TitleLabel.ExecProviderAdvancedDataForm.TLabel"
        ).grid(row=0, column=2, sticky='nsw')
        self._args_count_lb.grid(row=0, column=3, sticky='nsw')
        self._provider_args_field.grid(row=1, column=2, columnspan=2, rowspan=4, sticky='nswe')

        #
        self.grid_columnconfigure([0, 3], weight=1)

        #
        self._register_field(self._provider_binary_entry)
        self._register_field(self._provider_lang_template_entry)
        self._register_field(self._provider_args_field)

    def _set_style(self):
        self.config()
        Style().configure(
            "TitleLabel.ExecProviderAdvancedDataForm.TLabel",
            font=(self._font[0], self._font[1] + 1, "bold")
        )

    def _bind_events(self):
        self._retrieve_binary_btn.config(command=self._get_binary_path)
        self._provider_args_field.on_changed = lambda i : self._args_count_lb.configure(text=f"({len(i)})")

    def _get_binary_path(self):
        path = filedialog.askopenfilename(
            filetypes=[("All", "*"), ("Executable", "*.exe"), ("Binaire", "*.out")]
        )
        #
        if not path: return
        #
        if not path.strip():
            raise ValueError("binary path can't be empty.")
        #
        self._provider_binary_entry.text = path

    def read_only(self, value : bool):
        self._retrieve_binary_btn.config(state="disabled" if value else "normal")
        super().read_only(value)

    def enable(self):
        self.read_only(False)

    def disable(self):
        self.read_only(True)


if __name__ == "__main__" :
    root = Tk()
    root.geometry("500x400")
    widget = ExecProviderAdvancedDataForm(root, "exec_form",font=("Ubuntu", 12))
    widget.pack(fill='both', expand=True)
    widget.on_field_changed = lambda f, v : print(f, v)
    root.mainloop()