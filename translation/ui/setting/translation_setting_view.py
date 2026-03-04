import tkinter
from tkinter import Frame

from shared.ui.components.stack_frame import StackFrame
from translation.ui.setting.add_provider_frame import AddProviderFrame
from translation.ui.setting.provider_data_frame import ProviderDataFrame
from translation.ui.setting.provider_list_frame import ProviderListFrame


class TranslationSettingView(StackFrame):
    _PROVIDER_LIST_FRAME_ID = "provider_list_frame"
    _PROVIDER_DATA_FRAME_ID = "provider_data_frame"
    _ADD_PROVIDER_FRAME_ID = "add_provider_frame"
    #
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        #
        self._provider_list_frame = self.add_item(self._PROVIDER_LIST_FRAME_ID, ProviderListFrame)
        self._provider_data_frame = self.add_item(self._PROVIDER_DATA_FRAME_ID, ProviderDataFrame)
        self._add_provider_frame = self.add_item(self._ADD_PROVIDER_FRAME_ID, AddProviderFrame)
        #

    @property
    def provider_list_frame(self):
        return self._provider_list_frame

    @property
    def provider_data_form(self):
        return self._provider_data_frame

    @property
    def add_provider_frame(self):
        return self._add_provider_frame

if __name__ == "__main__" :
    root = tkinter.Tk()
    root.geometry("500x400")
    #
    view = TranslationSettingView(root)

    view.pack(fill='both', expand=True)
    #
    root.mainloop()