import tkinter as tk
from tkinter import Frame, Button
from shared.ui.components.stack_frame import StackFrame
from translation.ui.translation_frame import TranslationFrame


class CentralBar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.nav_bar = Frame(self, height=35, relief="sunken", border=1)
        self.stack = StackFrame(self)
        #
        self.nav_bar.pack(side="top", fill="x")
        self.stack.pack(side="top", fill="both", expand=True)

        # Create stacks
        self.trad_stack = self.stack.add_stack_item('trad')
        self.hist_stack = self.stack.add_stack_item('hist')
        self.config_stack = self.stack.add_stack_item('config')

        #Stack content
        self.trad_stack.config(bg="purple")
        self.translation_frame = TranslationFrame(self.trad_stack)

        #
        self.translation_frame.pack(fill="both", expand=True)

        # Add label inside each stack to visualize
        # tk.Label(self.trad_stack, text="Page Traduire", bg="lightgreen").pack(expand=True)
        tk.Label(self.hist_stack, text="Page Historique", bg="lightgreen").pack(expand=True)
        tk.Label(self.config_stack, text="Page Configuration", bg="lightgreen").pack(expand=True)

        buttons = {
            "Traduire": "trad",
            "Historique": "hist",
            "Configuration": "config"
        }

        for text, tag in buttons.items():
            btn = Button(self.nav_bar, text=text, cursor="hand2")
            btn.pack(padx=1 , pady=1, side="left")
            btn.bind("<Button-1>", lambda e, t = tag: self.on_switch_bt_clicked(tag=t, event=e))

    def on_switch_bt_clicked(self, tag, event):
        self.stack.show_child(tag)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x500")
    central = CentralBar(root)
    central.pack(fill="both", expand=True)
    root.mainloop()
