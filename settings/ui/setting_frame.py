import tkinter
from tkinter import Frame
from tkinter.ttk import Label, Button, Style


from shared.ui.components.scroll_pane import ScrollPane
from shared.ui.components.stack_frame import StackFrame


class SettingFrame(Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        #
        self._title_pane = Frame(self, bg="light gray", height=75)
        self._title_pane.pack_propagate(False)
        #
        self._title_lb = Label(self._title_pane, text="Paramètres", font=("Ubuntu", 24, "bold"), background=self._title_pane["bg"])
        #
        self._content_pane = Frame(self, background="light gray", pady=2, padx=1)
        #
        self._configs_list_scroll = ScrollPane(self._content_pane, background="#f4f4f4", width=180, borderwidth=2, relief="raised")
        #
        self._configs_list_pane = self._configs_list_scroll.pane
        self._configs_list_pane.config(padx=1, pady=2)
        #
        self._configs_stack = StackFrame(self._content_pane, padding=3)
        #
        self._title_pane.pack(side="top", fill="x")
        self._title_lb.pack(side="left", padx=10)
        #
        self._content_pane.pack(side="top", fill="both", expand=True)
        #
        self._configs_list_scroll.pack(side="left", fill="y")
        self._configs_stack.pack(side="left", fill="both", expand=True)


    ###################################### GETTERS AND SETTERS ############################################
    @property
    def configs_stack(self):
        return self._configs_stack

    @property
    def configs_list_pane(self):
        return self._configs_list_pane

if __name__ == "__main__":
    root = tkinter.Tk()
    root.geometry("500x500")
    central = SettingFrame(root)
    central.pack(fill="both", expand=True)
    root.mainloop()

