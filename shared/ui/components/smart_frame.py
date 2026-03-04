from tkinter.ttk import Frame

from shared.ui.mixins.smart_events import SmartEventMixin


class SmartFrame(Frame, SmartEventMixin):
    def __init__(self, master, **kwargs):
        Frame.__init__(self, master, **kwargs)
        SmartEventMixin.__init__(self)