import tkinter as tk

from translation.ui.components.provider_combobox import ProviderCombobox


class TopBar(tk.Frame):

    def __init__(self, parent, app_name, **kwargs):
        super().__init__(parent, bg="white", **kwargs)
        self.config(padx=10, pady=10)
        self.app_name_label = tk.Label(self, bg=self["bg"], text=app_name, font=("Ubuntu", 24, "bold"))
        self.provider_selector = ProviderCombobox(self, height=75, width=200)
        #
        self.app_name_label.pack(side="left")
        self.provider_selector.pack(side="right", anchor="e")


if __name__ == "__main__" :
    root = tk.Tk()
    entry = TopBar(root, "Testic")
    entry.pack(side='top', fill='x')
    root.mainloop()

