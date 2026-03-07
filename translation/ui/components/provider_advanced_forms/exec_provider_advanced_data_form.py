import os
from tkinter import Tk, filedialog, StringVar
from tkinter.ttk import Style, Label, Button, Frame
from typing import Tuple

from shared.infra.utils.image_utils import ImageUtils
from shared.ui.components.dict_view import DictView
from shared.ui.components.form_field_widgets import EntryField
from translation.ui.components.provider_advanced_data_form import ProviderAdvancedDataForm


class ExecProviderAdvancedDataForm(ProviderAdvancedDataForm):
    PROVIDER_BINARY_FIELD = "provider_binary"
    PROVIDER_LANG_TEMPLATE_FIELD = "provider_lang_template"
    PROVIDER_ARGS_FIELD = "provider_args"
    #
    _FOLDER_IMG_PATH = os.path.join(os.path.dirname(__file__), "../../../resources/icons8-folder-100-2.png")

    def __init__(
            self,
            master,
            name,
            font : Tuple[str, int] | Tuple[str, int, str] = ("", 11),
            readonly : bool = False,
            required : bool = True,
            **kwargs
    ):
        super().__init__(master, name, required, **kwargs)
        #
        self._font = font
        self._binary_path = StringVar(self, "")
        self._folder_img = ImageUtils.get_tk_image(self._FOLDER_IMG_PATH, 22)
        #
        self._build_ui()
        self._set_style()
        self._bind_events()
        #
        self.readonly = readonly

    def _build_ui(self):
        _left_pane = Frame(self)
        _right_pane = Frame(self)
        #
        _binary_pane = Frame(_left_pane)
        #
        self._provider_binary_entry = EntryField(
            _binary_pane,
            self.PROVIDER_BINARY_FIELD,
            placeholder="Ex : /usr/bin/translator",
            font=self._font,
            style="Entry.ExecProviderAdvancedDataForm.TEntry",
        )
        #
        self._retrieve_binary_btn = Button(
            _binary_pane,
            image=self._folder_img,
            padding=0,
            style="Button.ExecProviderAdvancedDataForm.TButton",
            cursor="hand2"
        )
        #
        self._provider_lang_template_entry = EntryField(
            _left_pane,
            self.PROVIDER_LANG_TEMPLATE_FIELD,
            placeholder="Ex : @src_lang:@target_lang",
            font=self._font,
            style="Entry.ExecProviderAdvancedDataForm.TEntry"
        )
        #
        self._provider_args_field = DictView(
            _right_pane,
            "Arguments",
            self.PROVIDER_ARGS_FIELD,
            key_name="Argument",
            value_name="Valeur",
            font=self._font,
            allow_empty_value=True,
            allow_repeated_value=True,
        )

        # --- Displaying -------------------------------------------
        _left_pane.pack(side='left', expand=True, fill='both')
        _right_pane.pack(side='right', expand=True, fill='both')
        #
        Label(
            _left_pane,
            text="Chemin de l'exécutable",
            style="TitleLabel.ExecProviderAdvancedDataForm.TLabel"
        ).pack(side='top', fill='x', pady=(2, 1))
        #
        _binary_pane.pack(side='top', fill='x', pady=(1, 4))
        #
        self._provider_binary_entry.pack(side='left', fill='x', expand=True)
        self._retrieve_binary_btn.pack(side='right', fill='both', padx=3)

        #
        Label(
            _left_pane,
            text="Template de langue",
            style="TitleLabel.ExecProviderAdvancedDataForm.TLabel"
        ).pack(side='top', fill='x', pady=(5, 1))
        #
        self._provider_lang_template_entry.pack(side='top', fill='x', pady=1)
        #
        self._provider_args_field.pack(fill='both', expand=True)

        #
        self._register_field(self._provider_binary_entry)
        self._register_field(self._provider_lang_template_entry)
        self._register_field(self._provider_args_field)

    def _set_style(self):
        self.config()
        Style().configure(
            "TitleLabel.ExecProviderAdvancedDataForm.TLabel",
            font=(self._font[0], self._font[1] + 1, "bold"),
            padding=(1, 3)
        )

    def _bind_events(self):
        self._retrieve_binary_btn.config(command=self._get_binary_path)

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

    def set_readonly(self, value: bool):
        self._retrieve_binary_btn.config(state="disabled" if value else "normal")
        super().set_readonly(value)

    def _enable(self):
        self.readonly = False

    def _disable(self):
        self.readonly = True


if __name__ == "__main__" :
    root = Tk()
    root.geometry("500x400")
    widget = ExecProviderAdvancedDataForm(root, "exec_form",font=("Ubuntu", 12))
    widget.pack(fill='both', expand=True)
    widget.readonly = True
    widget.on_field_changed = lambda f, v : print(f, v)
    root.mainloop()