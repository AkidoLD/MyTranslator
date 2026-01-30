import tkinter as tk


class FloatFrame(tk.Toplevel):

    def __init__(self, parent, is_hide : bool = True, **kwargs):
        super().__init__(parent, **kwargs)
        self.overrideredirect(True)
        self.attributes("-topmost", False)
        #
        if is_hide : self.hide()
        else : self.show()

    def is_display(self):
        return self.winfo_ismapped()

    def hide(self):
        self.withdraw()

    def show(self):
        self.deiconify()


    def toggle_menu(self):
        if self.is_display():
            self.hide()
        else:
            self.show()

    def resize(self, w :float, h : float):
        self.geometry(f"{w}x{h}")

    def move_to(self, x : float, y : float):
        self.geometry(f"+{x}+{y}")

