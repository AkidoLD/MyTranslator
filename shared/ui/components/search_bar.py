import os.path
import tkinter
from tkinter.ttk import Frame, Button, Style
from typing import Tuple, Callable

from shared.infra.utils.image_utils import ImageUtils
from shared.ui.components.advanced_entry import AdvancedEntry


class SearchBar(Frame):
    _SEARCH_IMG_PATH = os.path.join(os.path.dirname(__file__), "../../resources/icons8-search-100-2.png")

    def __init__(
            self,
            master,
            background: str = "white",
            font: Tuple[str, int, str] | Tuple[str, int] = None,
            placeholder: str = None,
            on_search: Callable[[str], None] | None = None,
            **kwargs
    ):
        super().__init__(master, style="SearchBar.TFrame", **kwargs)
        #
        self._last_height = 0
        self._search_image = ImageUtils.get_image(self._SEARCH_IMG_PATH)
        #
        self._configure_styles(background)
        self._build_ui(font, placeholder, background)
        #
        self.on_search = on_search
        #
        self.bind("<Configure>", lambda _: self._update_icon())

    def _configure_styles(self, background: str):
        Style(self).configure("SearchBar.TFrame", background=background)
        #
        Style(self).configure(
            "Button.SearchBar.TButton",
            padding=(0, 0),
            borderwidth=0,
            background="#a8a8a8",
            relief="raised",
            highlightthickness=0
        )
        Style(self).map(
            "Button.SearchBar.TButton",
            background=[
                ("active", "#666666")
            ]
        )

        #
        Style(self).configure(
            "Entry.SearchBar.TEntry",
            padding=(3, 1),
            borderwidth=0,
            background="#a8a8a8",
            relief="raised",
            highlightthickness=0
        )

    def _build_ui(self, font, placeholder, background):
        self._search_btn = Button(self, style="Button.SearchBar.TButton", command=self._handle_search, cursor="hand2")
        self._search_entry = AdvancedEntry(self, placeholder=placeholder, font=font, background=background, style="Entry.SearchBar.TEntry")
        #
        self._search_entry.bind("<Return>", lambda _: self._handle_search())
        self._search_entry.bind("<KP_Enter>", lambda _: self._handle_search())
        #
        self._search_btn.pack(side="left", fill="both")
        self._search_entry.pack(fill="x", expand=True)

    def _handle_search(self):
        query = self._search_entry.get()
        if self._on_search is not None:
            self._on_search(query)

    def _update_icon(self):
        h = self.winfo_height()
        #
        if h == self._last_height or h <= 1:
            return
        #
        self._last_height = h
        img_size = h - 3
        #
        self._search_btn_img = ImageUtils.convert_to_tk_image(self._search_image, (img_size, img_size))
        self._search_btn.config(image=self._search_btn_img)

    def get(self):
        return self._search_entry.get()

    def clear(self):
        self._search_entry.text = ""

    @property
    def on_search(self) -> Callable[[str], None] | None:
        return self._on_search

    @on_search.setter
    def on_search(self, callback: Callable[[str], None] | None) -> None:
        if callback is not None and not callable(callback):
            raise TypeError(f"on_search must be callable or None, git type: {type(callback).__name__}")
        #
        self._on_search = callback


if __name__ == "__main__":
    root = tkinter.Tk()
    root.geometry("500x100")
    root.title("SearchBar Test")
    #
    bar = SearchBar(root, font=("Ubuntu", 14, "bold"), placeholder="Rechercher...", on_search=lambda q: print(f"Recherche : {q}"))
    bar.pack(fill="x", padx=10, pady=10)
    #
    root.mainloop()