import tkinter as tk


class CircleWidget(tk.Canvas):
    def __init__(self, parent, diameter : float = 10, color : str = "white", outline : str = "black", width : int = 1, **kwargs):
        super().__init__(parent, highlightthickness=0, **kwargs)
        self._diameter = diameter
        self.config(width=diameter, height=diameter)
        self._color = color
        self._outline = outline
        self._width = width
        self._circle = None

        #Bind the drawing callback
        self.bind("<Configure>", self.draw_circle)

    def draw_circle(self, event = None):
        #Erase the circle if it is already draw
        if self._circle :
            self.delete(self._circle)

        #Calculate the circle position
        w, h = self.winfo_width(), self.winfo_height()
        x0 , y0 = (w - self._diameter) / 2, (h - self._diameter) / 2
        x1 , y1 = x0 + self._diameter, y0 + self._diameter

        #Draw a new circle with the new dimension and position
        self._circle = self.create_oval(x0, y0, x1, y1, fill=self._color, outline=self._outline, width=self._width)

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value: str):
        self._color = value
        self.draw_circle()

    @property
    def outline(self):
        return self._outline

    @outline.setter
    def outline(self, value: str):
        self._outline = value
        self.draw_circle()

    @property
    def diameter(self):
        return self._diameter

    @diameter.setter
    def diameter(self, value : float):
        self._diameter = value
        self.draw_circle()

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value : float):
        self._width = value
        self.draw_circle()