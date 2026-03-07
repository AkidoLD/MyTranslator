import os.path
import tkinter
from tkinter.ttk import Frame, Button, Label, Style
from typing import Callable, List

from shared.infra.services.tk_dialog_service import TkDialogService
from shared.infra.utils.image_utils import ImageUtils
from shared.infra.utils.validation_utils import validate_callable, validate_type
from shared.ui.components.scroll_pane import ScrollPane
from shared.ui.components.search_bar import SearchBar
from translation.ui.components.trans_provider_data import TransProviderData
from translation.ui.components.trans_provider_widget import TransProviderWidget

class _NoProviderWidget(tkinter.Frame, TkDialogService):
    def __init__(self, master, **kwargs):
        super().__init__(master, height=35, bd=2, relief='solid', cursor='hand2', **kwargs)
        #
        self.pack_propagate(False)
        Label(self, text="Aucun fournisseur trouve.", anchor="center", font=("Ubuntu", 14, "bold")).pack(fill='x', expand=True)
        

class ProviderListFrame(Frame):
    _ADD_IMG_PATH = os.path.join(os.path.dirname(__file__), "../../resources/icons8-plus-math-100.png")
    _REFRESH_IMG_PATH = os.path.join(os.path.dirname(__file__), "../../resources/icons8-synchronize-100.png")

    def __init__(
            self,
            master,
            on_add_btn_clicked: Callable | None = None,
            on_refresh_btn_clicked: Callable | None = None,
            on_search: Callable[[str], None] | None = None,
            on_provider_clicked: Callable[[str], None] | None = None,
            on_provider_deleted: Callable[[str], None] | None = None,
            **kwargs
    ):
        super().__init__(master, **kwargs)
        #
        self._provider_count = 0
        #
        self._add_img = ImageUtils.get_tk_image(self._ADD_IMG_PATH, 35)
        self._refresh_img = ImageUtils.get_tk_image(self._REFRESH_IMG_PATH, 22)
        #
        self._configure_styles()
        self._build_ui()
        #
        self.on_add_btn_clicked = on_add_btn_clicked
        self.on_refresh_btn_clicked = on_refresh_btn_clicked
        self.on_search = on_search
        self.on_provider_clicked = on_provider_clicked
        self.on_provider_deleted = on_provider_deleted

    def _configure_styles(self):
        Style().configure("ProviderListFrame.TFrame", background="white")
        Style().configure("TitlePane.TFrame", background="#dddddd")
        Style().configure("OptionPane.TFrame", background="white")
        Style().configure("TitleLabel.TLabel", font=("Ubuntu", 20, "bold"), background="#dddddd")
        Style().configure("AddProviderBtn.TButton", font=("Arial", 16, "bold"), space=10, background="#b8deff")
        Style().map("AddProviderBtn.TButton", background=[("active", "#82cdff")])
        #
        self.config(style="ProviderListFrame.TFrame")

    def _build_ui(self):
        # Title
        title_pane = Frame(self, height=75, style="TitlePane.TFrame")
        title_pane.pack_propagate(False)
        title_pane.pack(side="top", fill="x")
        #
        Label(title_pane, text="Liste des fournisseurs", style="TitleLabel.TLabel").pack(side="left", padx=5)
        self._provider_count_lb = Label(title_pane, style="TitleLabel.TLabel")
        self._provider_count_lb.pack(side="left", padx=(0, 5))

        # Options
        option_pane = Frame(self, style="OptionPane.TFrame")
        option_pane.pack(side="top", anchor="e")
        #
        self._refresh_btn = Button(option_pane, image=self._refresh_img, command=self._handler_refresh, padding=(2, 0), cursor="hand2")
        self._refresh_btn.pack(side="left", padx=(0, 5), fill='both')
        #
        self._search_bar = SearchBar(option_pane, background="white", font=("Ubuntu", 14), placeholder="Rechercher ...")
        self._search_bar.pack(fill="x", expand=True)

        # Content
        content_scroll = ScrollPane(self, background="white")
        content_scroll.pack(fill="both", expand=True)
        self._content_pane = content_scroll.pane
        self._content_pane.configure(bg="white")

        # Add button
        Button(
            self,
            text="Ajouter un fournisseur",
            style="AddProviderBtn.TButton",
            command=self._handler_add_provider,
            image=self._add_img,
            compound="left",
            cursor = "hand2",
            padding=0
        ).pack(side="bottom", fill="x")

        #No provider widget
        self._no_provider_widget = _NoProviderWidget(self._content_pane)

    # ─── Handlers internes ────────────────────────────────────────────────────

    def _handler_add_provider(self):
        if self._on_add_btn_clicked:
            self._on_add_btn_clicked()

    def _handler_refresh(self):
        if self._on_refresh_btn_clicked:
            self._on_refresh_btn_clicked()

    def _handler_provider_clicked(self, provider_id: str):
        if self._on_provider_clicked:
            self._on_provider_clicked(provider_id)

    def _handler_provider_deleted(self, provider_id: str):
        if self._on_provider_deleted:
            self._on_provider_deleted(provider_id)

    # ─── Public API ─────────────────────────────────────────────────────────

    def clear_search_bar(self):
        self._search_bar.clear()

    def add_provider(self, provider: TransProviderData):
        TransProviderWidget(self._content_pane, provider.provider_id, provider.provider_name, provider.provider_type,
                            provider.provider_lang_count, provider.provider_req_internet,
                            on_clicked=self._handler_provider_clicked,
                            on_delete_btn_clicked=self._handler_provider_deleted).pack(side="top", fill="x", padx=1, pady=2)
        #
        self.provider_count = self.provider_count + 1
        if self.provider_count <= 1 and self._no_provider_widget.winfo_manager() : self._no_provider_widget.pack_forget()

    def add_providers(self, providers: List[TransProviderData]):
        for provider in providers:
            self.add_provider(provider)

    def set_providers(self, providers: List[TransProviderData]):
        self.clear_providers()
        self.add_providers(providers)

    def remove_provider(self, provider_id: str):
        for widget in self._content_pane.winfo_children():
            if isinstance(widget, TransProviderWidget) and widget.provider_id == provider_id:
                widget.destroy()
                self.provider_count = self.provider_count - 1
                if not self.provider_count and not self._no_provider_widget.winfo_manager():
                    self._no_provider_widget.pack(side='top' ,fill='x', padx=1, pady=2)
                return
        # raise ValueError(f"No TransProviderWidget with id {provider_id}.")

    def clear_providers(self):
        for child in self._content_pane.winfo_children() :
            if not isinstance(child, _NoProviderWidget) :  child.destroy()
        #
        self.provider_count = 0
        self._no_provider_widget.pack(side='top', fill='x', padx=1, pady=2)

    # ─── Properties ───────────────────────────────────────────────────────────
    @property
    def provider_count(self):
        return self._provider_count

    @provider_count.setter
    def provider_count(self, value):
        validate_type(value, int, "provider_count")
        self._provider_count = value
        self._provider_count_lb.config(text=f"({value})")

    @property
    def on_add_btn_clicked(self) -> Callable | None:
        return self._on_add_btn_clicked

    @on_add_btn_clicked.setter
    def on_add_btn_clicked(self, value: Callable | None):
        self._on_add_btn_clicked = validate_callable(value, "on_add_btn_clicked")

    @property
    def on_refresh_btn_clicked(self) -> Callable | None:
        return self._on_refresh_btn_clicked

    @on_refresh_btn_clicked.setter
    def on_refresh_btn_clicked(self, value: Callable | None):
        self._on_refresh_btn_clicked = validate_callable(value, "on_refresh_btn_clicked")

    @property
    def on_search(self) -> Callable[[str], None] | None:
        return self._search_bar.on_search

    @on_search.setter
    def on_search(self, value: Callable[[str], None] | None):
        self._search_bar.on_search = value

    @property
    def on_provider_clicked(self) -> Callable[[str], None] | None:
        return self._on_provider_clicked

    @on_provider_clicked.setter
    def on_provider_clicked(self, value: Callable[[str], None] | None):
        self._on_provider_clicked = validate_callable(value, "on_provider_clicked")

    @property
    def on_provider_deleted(self) -> Callable[[str], None] | None:
        return self._on_provider_deleted

    @on_provider_deleted.setter
    def on_provider_deleted(self, value: Callable[[str], None] | None):
        self._on_provider_deleted = validate_callable(value, "on_provider_deleted")


if __name__ == "__main__":
    import random
    import uuid
    root = tkinter.Tk()
    root.geometry("500x500")
    root.title("ProviderListFrame Test")

    frame = ProviderListFrame(
        root,
        on_refresh_btn_clicked=lambda: print("Refresh clicked"),
        on_search=lambda q: print(f"Recherche : {q}"),
        on_provider_clicked=lambda pid: print(f"Provider clicked : {pid}"),
        on_provider_deleted=lambda pid: print(f"Provider deleted : {pid}"),
    )
    frame.pack(fill="both", expand=True)

    frame.on_add_btn_clicked = lambda : frame.add_provider(TransProviderData(
        str(uuid.uuid4()),
        f"Provider {frame.provider_count}",
        "Fake",
        random.randint(0, 10),
        bool(random.randint(0, 1))
    ))

    frame.on_provider_deleted = lambda p_id : frame.after(200, frame.remove_provider, p_id)

    frame.add_providers([
        TransProviderData("1", "Google", "HTTP", 50),
        TransProviderData("2", "DeepL", "HTTP", 30),
    ])

    root.mainloop()