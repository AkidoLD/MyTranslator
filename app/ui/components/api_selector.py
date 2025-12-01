import tkinter as tk
from tkinter import Label

from duplicity.config import select_files

from app.ui.components.circle_widget import CircleWidget
from app.ui.components.float_menu import FloatMenu


class ApiStatusCircle(CircleWidget):
    def __init__(self, parent, diameter : float, status : bool = False):
        super().__init__(parent, diameter, outline="")
        self.status = status

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value
        self.color = "green" if self._status else "blue"

class ApiStatusWidget(tk.Frame):
    def __init__(self, parent, status=False):
        super().__init__(parent)
        self._status = status

        self.status_label = Label(self, text=self._label_text())
        self.status_indicator = ApiStatusCircle(self, 15, status)

        self.status_label.pack(side="left")
        self.status_indicator.pack(side="left", padx=2)

    def _label_text(self):
        return "Online" if self._status else "Offline"

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value
        self.status_label.config(text=self._label_text())
        self.status_indicator.status = value

class ApiSelectorItems(tk.Frame):
    def __init__(self, parent, name : str, status : bool):
        super().__init__(parent)
        self.api_name = tk.Label(self, text=name)
        self.api_status = ApiStatusCircle(self, 20, status)
        #
        self.api_name.pack(side="left", padx=(8, 0))
        self.api_status.pack(side="right", padx=(0, 8))
        self.config(bg="lightgray")
        self.config(height=20)

class ApiSelectorWidget(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        #
        Label(self, text="Service :", background=self["bg"]).grid(row=0, column=0, padx=5, pady=(5, 10))
        self.selected_api_name = Label(self, text="Not selected", background=self['bg'])
        self.selected_api_name.grid(row=0, column=1, pady=(5, 10), padx=10)
        self.selected_api_status = ApiStatusWidget(self)
        self.selected_api_status.grid(row=1, column=1, sticky="e", pady=(10, 0))

        #Create and configure the floating menu
        self.menu = FloatMenu(self)
        self.menu.config(background="lightgray")
        self.menu.bind("<FocusOut>", self.on_focus_out)
        self.menu.bind_all("<Configure>", self.on_configure)
        self.bind("<Button-1>", self.on_clicked)
        for w in self.winfo_children():
            w.bind("<Button-1>", self.on_clicked)

        w = ApiSelectorItems(self.menu, "Google", True)
        w1 = ApiSelectorItems(self.menu, "Trans", False)
        w.bind("<Button-1>", lambda  e: self.selected_api("Google"))
        w1.bind("<Button-1>", lambda e: self.selected_api("Translate"))
        w.pack(side="top", fill="x", expand=True, pady=2)
        w1.pack(fill="x", expand=True, pady=2)

    def on_focus_out(self, event = None):
        self.menu.hide()

    def on_configure(self, event = None):
        self._update_menu_pos()

    def on_clicked(self, event = None):
        self._update_menu_pos()
        self.menu.toggle_menu()

    def _update_menu_pos(self):
        if not self.menu:
            return
        #
        self.menu.update_idletasks()
        w, h = self.winfo_width(), self.menu.winfo_reqheight()
        x, y = self.winfo_rootx(), self.winfo_rooty() + self.winfo_height() + 5
        self.menu.geometry(f"{w}x{h}+{x}+{y}")

    def selected_api(self, name):
        print("Api clique :", name)


if __name__ == "__main__":
    root = tk.Tk()
    root.config(background="white")
    root.geometry("500x700")
    selector = ApiSelectorWidget(root)
    selector.pack()
    root.mainloop()

