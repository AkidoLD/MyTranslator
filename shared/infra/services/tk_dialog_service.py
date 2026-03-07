

from tkinter import messagebox

from shared.application.interfaces.dialog_service import DialogService


class TkDialogService(DialogService):

    def confirm_dialog(self, title: str, message: str) -> bool:
        return messagebox.askyesno(title, message)

    def info_dialog(self, title: str, message: str):
        messagebox.showinfo(title, message)

    def error_dialog(self, title: str, message: str):
        messagebox.showerror(title, message)

    def warning_dialog(self, title: str, message: str):
        messagebox.showwarning(title, message)