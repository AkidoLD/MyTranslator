import tkinter
from tkinter.ttk import Frame, Label, Style
from typing import Tuple, Literal

from shared.infra.utils.validation_utils import validate_type, validate_not_empty


class TitledFrame(Frame):
    def __init__(
            self,
            master,
            title : str,
            background : str = "gray",
            foreground : str = "black",
            anchor : Literal["nw", "n", "ne", "w", "center", "e", "sw", "s", "se"] = "w",
            font : Tuple[str, int] | Tuple[str, int, str] = ("", 14, "bold"),
            style : str = 'TitlePane.TitledFrame.TFrame',
            padx : int | tuple[int, int]= 1,
            pady : int | tuple[int, int]= 1,
            **kwargs
    ):
        super().__init__(master, **kwargs)
        #Set default style
        Style().configure(style, background=background)
        #
        #Build UI
        self._title_pane = Frame(self, style=style, padding=(2, 2))
        self._content_pane = Frame(self)
        #
        self._title_lb = Label(
            self._title_pane,
            text=title,
            font=font,
            foreground=foreground,
            background=background,
            anchor=anchor
        )
        #
        self._title_pane.pack(side='top', fill='x')
        self._title_lb.pack(fill='x', anchor=anchor)
        #
        self._content_pane.pack(side='top', fill='both', expand=True, padx=padx, pady=pady)

    @property
    def pane(self):
        return self._content_pane

    @property
    def title(self):
        return self._title_lb.cget('text')

    @title.setter
    def title(self, value : str):
        validate_type(value, str, "title")
        validate_not_empty(value, "title")
        self._title_lb.config(text=value)


if __name__ == "__main__":
    root = tkinter.Tk()
    root.geometry("500x500")
    central = TitledFrame(root, "Titled Frame", font=("Arial", 16, "bold"), borderwidth=1, relief="groove")
    central.pane.config(style="CustomPane.TFrame")
    Style().configure("CustomPane.TFrame", background="light yellow")
    central.pack(fill="both", expand=True, padx=2, pady=2)
    print(Style().layout("TLabel"))
    print(Style().element_options("TLabel.label"))
    root.mainloop()