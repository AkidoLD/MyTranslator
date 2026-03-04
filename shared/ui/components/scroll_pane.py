import tkinter
from enum import Enum
from tkinter import Canvas, Misc, Frame
from tkinter.ttk import Scrollbar


class ScrollPolicy(Enum):
    NEVER = 1
    ALWAYS = 2
    AUTO = 3


class ScrollPane(Frame):
    HBAR_POS = (1, 0)
    VBAR_POS = (0, 1)

    def __init__(
            self,
            master: Misc | None = None,
            hbar_policy: ScrollPolicy = ScrollPolicy.AUTO,
            vbar_policy: ScrollPolicy = ScrollPolicy.AUTO,
            fit_width: bool = True,
            fit_height: bool = False,
            background: str = "white",
            **kwargs
    ):
        super().__init__(master, bg=background, **kwargs)
        #
        self._hbar_policy = hbar_policy
        self._vbar_policy = vbar_policy
        self._fit_width = fit_width
        self._fit_height = fit_height
        self._background = background
        #
        self._build_ui()
        self._bind_events()
        self._update_content()

    def _build_ui(self):
        self.grid_propagate(False)
        #
        self._canvas = Canvas(self, highlightthickness=0, bg=self._background)
        self._hbar = Scrollbar(self, orient="horizontal", command=self._canvas.xview)
        self._vbar = Scrollbar(self, orient="vertical", command=self._canvas.yview)
        self._pane = Frame(self._canvas, bg=self._background)
        #
        self._canvas.config(
            yscrollcommand=self._vbar.set,
            xscrollcommand=self._hbar.set
        )
        #
        self._canvas.grid(row=0, column=0, sticky="nsew")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        #
        self._scroll_window = self._canvas.create_window(
            (0, 0),
            window=self._pane,
            anchor="nw"
        )

    def _bind_events(self):
        self._canvas.bind("<Configure>", self._on_canvas_configure, "+")
        self._pane.bind("<Configure>", self._on_pane_configure, "+")

    def _on_canvas_configure(self, event):
        if self._fit_width:
            self._canvas.itemconfig(self._scroll_window, width=event.width)
        if self._fit_height:
            self._canvas.itemconfig(self._scroll_window, height=event.height)
        self._update_content()

    def _on_pane_configure(self, _):
        self._update_content()

    @staticmethod
    def _check_scrollbar_visibility(policy: ScrollPolicy, content: int, container: int) -> bool:
        if policy == ScrollPolicy.NEVER:
            return False
        if policy == ScrollPolicy.ALWAYS:
            return True
        return content > container

    def _update_scrollbar_visibility(self):
        show_hbar = not self._fit_width and self._check_scrollbar_visibility(
            self._hbar_policy, self._pane.winfo_reqwidth(), self._canvas.winfo_width()
        )
        show_vbar = not self._fit_height and self._check_scrollbar_visibility(
            self._vbar_policy, self._pane.winfo_reqheight(), self._canvas.winfo_height()
        )
        #
        if show_hbar:
            self._hbar.grid(row=self.HBAR_POS[0], column=self.HBAR_POS[1], sticky="we")
        else:
            self._hbar.grid_forget()
        #
        if show_vbar:
            self._vbar.grid(row=self.VBAR_POS[0], column=self.VBAR_POS[1], sticky="ns")
        else:
            self._vbar.grid_forget()

    def _update_content(self):
        self._canvas.configure(scrollregion=self._canvas.bbox("all"))
        self._update_scrollbar_visibility()

    @property
    def pane(self) -> Frame:
        return self._pane


if __name__ == "__main__":
    from tkinter.ttk import Button
    root = tkinter.Tk()
    root.geometry("500x500")
    root.title("Test ScrollPane")
    #
    scroll = ScrollPane(root, background="white")
    scroll.pack(fill="both", expand=True)
    #
    for i in range(20):
        Button(scroll.pane, text=f"Button {i} - Un texte plus long pour tester").pack(
            side="top", fill="x", padx=5, pady=2
        )
    #
    root.mainloop()