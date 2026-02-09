from tkinter import Frame


class BorderedFrame(Frame):
    def __init__(
            self,
            master,
            background : str = "white",
            border : int = 0,
            border_color : str = "black",
            **kwargs
    ):
        super().__init__(master, **kwargs)
        #
        self.config(background=border_color, pady=border, padx=border)
        self._pane = Frame(self, bg=background)
        self._pane.pack(fill="both", expand=True)

    @property
    def border(self) -> int :
        return self.cget("padx")

    @border.setter
    def border(self, value : int):
        self.config(padx=value, pady=value)

    @property
    def border_color(self):
        return self.cget("bg")

    @border_color.setter
    def border_color(self, value : str):
        self.config(bg=value)

    @property
    def background(self):
        return self._pane.cget("bg")

    @background.setter
    def background(self, value : str):
        self._pane.config(bg=value)

    @property
    def pane(self):
        return self._pane

        
    
    