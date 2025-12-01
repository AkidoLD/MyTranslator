import tkinter as tk


class FloatMenu(tk.Toplevel):

    def __init__(self, parent):
        super().__init__(parent)
        # self.attributes("-topmost", True)
        self.attributes("-type", "dropdown_menu")
        self.attributes("-topmost", True)
        self.withdraw()
        if self.master:
            self.master.bind("<FocusOut>", lambda e: self.hide)

    def is_display(self):
        return self.winfo_ismapped()

    def hide(self):
        if self.is_display():
            self.withdraw()

    def show(self):
        if not self.is_display():
            self.deiconify()

    def toggle_menu(self):
        if self.is_display():
            self.hide()
        else:
            self.show()


if __name__ == "__main__" :
    root = tk.Tk()
    menu = FloatMenu(root)
    root.geometry("500x500")
    root.mainloop()

