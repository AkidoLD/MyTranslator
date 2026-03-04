from tkinter.ttk import Spinbox


class IntSpinBox(Spinbox):
    def __init__(self, master, from_: int = 0, to : int = 9999, **kwargs):
        super().__init__(master, **kwargs)
        #
        def _validate_spin_entry(new_value: str):
            return (new_value.isdigit()  and self.cget("from") <= int(new_value) <= self.cget("to"))or new_value == ""

        vcmd = self.register(_validate_spin_entry)
        self.config(
            validate="all",
            validatecommand=(vcmd, "%P")
        )