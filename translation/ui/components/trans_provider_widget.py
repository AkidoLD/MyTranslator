import os.path
import tkinter
import uuid
from tkinter import Frame
from tkinter.ttk import Label, Button, Style
from typing import Callable

from shared.infra.utils.image_utils import ImageUtils
from shared.infra.utils.validation_utils import validate_type, validate_not_empty, validate_callable
from shared.ui.components.smart_frame import SmartFrame
from translation.ui.components.provider_combobox_item import ProviderInternetReqCircle


class TransProviderWidget(Frame):

    _DELETE_IMG_PATH = os.path.join(os.path.dirname(__file__), "../../resources/icons8-trash-can-100.png")

    def __init__(
            self,
            master,
            provider_id: str,
            provider_name: str,
            provider_type: str,
            provider_lang_count: int = 0,
            provider_req_internet: bool = True,
            on_clicked: Callable[[str], None] | None = None,
            on_delete_btn_clicked: Callable[[str], None] | None = None,
            **kwargs
    ):
        super().__init__(master, bd=2, relief="solid", cursor="hand2", **kwargs)
        #
        self._configure_styles()
        self._delete_img = ImageUtils.get_tk_image(self._DELETE_IMG_PATH, (25, 25))
        #
        self._info_pane = SmartFrame(self)
        self._status_circle = ProviderInternetReqCircle(self._info_pane, provider_req_internet, diameter=15, width=1)
        self._provider_name_lb = Label(self._info_pane, style="ProviderName.TLabel")
        self._provider_type_lb = Label(self._info_pane, style="ProviderType.TLabel", width=0)
        self._lang_count_lb = Label(self._info_pane, style="ProviderLang.TLabel", width=0)
        self._delete_provider_btn = Button(self, style="DeleteProvider.TButton", image=self._delete_img)
        #
        self.provider_id = provider_id
        self.provider_status = provider_req_internet
        self.provider_name = provider_name
        self.provider_type = provider_type
        self.provider_lang_count = provider_lang_count
        self.on_clicked = on_clicked
        self.on_delete_btn_clicked = on_delete_btn_clicked
        #
        self._build_ui()

    # ─── Setup ────────────────────────────────────────────────────────────────

    def _configure_styles(self):
        Style(self).configure("ProviderName.TLabel", font=("Ubuntu", 14, "bold"))
        Style(self).configure("ProviderType.TLabel", font=("Arial", 14))
        Style(self).configure("ProviderLang.TLabel", font=("Ubuntu", 13, "bold"))
        Style(self).configure("DeleteProvider.TButton", background="#f05a5a", relief="raised", border=1)
        Style(self).map("DeleteProvider.TButton", background=[("active", "#fd3232")])

    def _build_ui(self):
        self._delete_provider_btn.pack(side="right", padx=(5, 0))
        self._lang_count_lb.pack(side="right", padx=5)
        self._provider_type_lb.pack(side="right", padx=10)
        self._info_pane.pack(side="left", fill="x", expand=True)
        self._status_circle.pack(side="left", padx=5)
        self._provider_name_lb.pack(side="left", padx=5)
        #
        self._info_pane.bind(SmartFrame.SMART_L_CLICK, lambda _: self._handler_on_clicked())
        self._delete_provider_btn.bind("<Button-1>", lambda _: self.after(0, self._handler_on_delete_btn_clicked))

    # ─── Handlers ─────────────────────────────────────────────────────────────

    def _handler_on_clicked(self):
        if self._on_clicked:
            self._on_clicked(self.provider_id)

    def _handler_on_delete_btn_clicked(self):
        if self._on_delete_btn_clicked:
            self._on_delete_btn_clicked(self.provider_id)

    # ─── Properties ───────────────────────────────────────────────────────────

    @property
    def provider_id(self) -> str:
        return self._provider_id

    @provider_id.setter
    def provider_id(self, value: str):
        self._provider_id = validate_not_empty(validate_type(value, str, "provider_id"), "provider_id")

    @property
    def provider_status(self) -> bool:
        return self._status_circle.req_internet

    @provider_status.setter
    def provider_status(self, value: bool):
        self._status_circle.req_internet = validate_type(value, bool, "provider_req_internet")

    @property
    def provider_name(self) -> str:
        return self._provider_name_lb.cget("text")

    @provider_name.setter
    def provider_name(self, value: str):
        self._provider_name_lb.config(text=validate_not_empty(validate_type(value, str, "provider_name"), "provider_name"))

    @property
    def provider_type(self) -> str:
        return self._provider_type_lb.cget("text")

    @provider_type.setter
    def provider_type(self, value: str):
        self._provider_type_lb.config(text=validate_not_empty(validate_type(value, str, "provider_type"), "provider_type"))

    @property
    def provider_lang_count(self) -> int:
        return self._lang_count

    @provider_lang_count.setter
    def provider_lang_count(self, value: int):
        self._lang_count = validate_type(value, int, "provider_lang_count")
        self._lang_count_lb.config(text=f"({value}) Langues")

    @property
    def on_clicked(self) -> Callable[[str], None] | None:
        return self._on_clicked

    @on_clicked.setter
    def on_clicked(self, value: Callable[[str], None] | None):
        self._on_clicked = validate_callable(value, "on_clicked")

    @property
    def on_delete_btn_clicked(self) -> Callable[[str], None] | None:
        return self._on_delete_btn_clicked

    @on_delete_btn_clicked.setter
    def on_delete_btn_clicked(self, value: Callable[[str], None] | None):
        self._on_delete_btn_clicked = validate_callable(value, "on_delete_btn_clicked")


if __name__ == "__main__":
    root = tkinter.Tk()
    root.geometry("500x100")
    root.title("TransProviderWidget Test")
    #
    TransProviderWidget(
        root, str(uuid.uuid4()), "Trans", "binary", 12, True,
        on_clicked=lambda _id: print(f"Provider {_id} clicked"),
        on_delete_btn_clicked=lambda _id: print(f"Provider {_id} deleted")
    ).pack(fill="x", padx=10, pady=10)
    #
    root.mainloop()