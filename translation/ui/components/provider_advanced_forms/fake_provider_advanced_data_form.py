from tkinter.ttk import Label

from translation.ui.components.provider_advanced_data_form import ProviderAdvancedDataForm


class FakeProviderAdvancedDataForm(ProviderAdvancedDataForm):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        #
        Label(self, text="Rien a configurer ici.").pack(side='top', fill='x')