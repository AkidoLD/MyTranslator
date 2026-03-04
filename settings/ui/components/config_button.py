import tkinter
from tkinter import Frame
from tkinter.ttk import Button, Style


class ConfigButton(Button):
    def __init__(self, master, **kwargs):
        super().__init__(master,**kwargs)
        #
        style = Style()
        font = ("Arial", 13, "bold")

        style.configure(
            "ConfigButton.TButton",
            background="white",
            foreground="black",
            anchor="w",
            padding=(10, 2),
            font=font
        )

        #
        style.map("ConfigButton.TButton",
                    background=[
                        ("active", "#dddddd"),
                        ("pressed", "#dddddd"),
                        ("disabled", "gray")
                    ],
                    foreground=[
                        ("disabled", "light gray")
                    ]
        )
        #
        self.config(style="ConfigButton.TButton")



if __name__ == "__main__" :
    root = tkinter.Tk()
    root.geometry("500x500")
    frame = Frame(root)
    #
    btn = ConfigButton(frame, text="Je suis un config button")
    btn.pack(side="top", fill="x")
    #
    frame.pack(fill="both", expand=True)

    root.mainloop()
