import tkinter

from shared.infra.services.tk_dialog_service import TkDialogService
from shared.ui.components.stack_frame import StackFrame
from translation.ui.setting.add_provider_frame import AddProviderFrame
from translation.ui.setting.provider_list_frame import ProviderListFrame
from translation.ui.setting.update_provider_frame import UpdateProviderFrame


class TranslationSettingFrame(StackFrame, TkDialogService):
    PROVIDER_LIST_FRAME = "provider_list_frame"
    UPDATE_PROVIDER_FRAME = "update_provider_frame"
    ADD_PROVIDER_FRAME = "add_provider_frame"
    #
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        #
        self._provider_list_frame : ProviderListFrame = self.add_item(self.PROVIDER_LIST_FRAME, ProviderListFrame)
        self._update_provider_frame : UpdateProviderFrame = self.add_item(self.UPDATE_PROVIDER_FRAME, UpdateProviderFrame)
        self._add_provider_frame : AddProviderFrame = self.add_item(self.ADD_PROVIDER_FRAME, AddProviderFrame)
        #

    def show_add_provider_frame(self):
        self.raise_item(self.ADD_PROVIDER_FRAME)

    def show_provider_list_frame(self):
        self.raise_item(self.PROVIDER_LIST_FRAME)

    def show_update_provider_frame(self):
        self.raise_item(self.UPDATE_PROVIDER_FRAME)

    @property
    def provider_list_frame(self):
        return self._provider_list_frame

    @property
    def update_provider_frame(self):
        return self._update_provider_frame

    @property
    def add_provider_frame(self):
        return self._add_provider_frame

if __name__ == "__main__" :
    root = tkinter.Tk()
    root.geometry("500x400")
    #
    view = TranslationSettingFrame(root)

    view.pack(fill='both', expand=True)
    #
    root.mainloop()