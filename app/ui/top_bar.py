import tkinter as tk

from translation.ui.components.api_combobox import ApiComboBox


class TopBar(tk.Frame):

    def __init__(self, parent, app_name, **kwargs):
        super().__init__(parent, bg="white", **kwargs)
        self.config(padx=10, pady=10)
        self.app_name_label = tk.Label(self, bg=self["bg"], text=app_name, font=("Ubuntu", 24, "bold"))
        self.app_select_api = ApiComboBox(self, height=75, width= 200, bg="gray")
        #
        self.app_name_label.pack(side="left")
        self.app_select_api.pack(side="right", anchor="e")



