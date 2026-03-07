import tkinter as tk
from tkinter import Misc
from tkinter.ttk import Frame
from typing import Tuple

from shared.infra.utils.validation_utils import validate_type


class FloatFrame(Frame):

    def __init__(
            self,
            master : Misc | None = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        self.master = master