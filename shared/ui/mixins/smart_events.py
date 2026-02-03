from tkinter import Widget, Event, EventType, Label, Tk, Frame, Button, Entry

from typing import TypeVar, Self

from sympy import false

T = TypeVar("T", bound=Widget)


class SmartEventMixin:

    SMART_ENTER = "<<SmartEnter>>"
    SMART_LEAVE = "<<SmartLeave>>"
    SMART_CLICK = "<<SmartClick>>"
    SMART_L_CLICK = "<<SmartLClick>>"
    SMART_R_CLICK = "<<SmartRClick>>"
    SMART_C_CLICK = "<<SmartCClick>>"
    SMART_MOTION = "<<SmartMotion>>"
    SMART_FOCUS_IN = "<<SmartFocusIn>>"
    SMART_FOCUS_OUT = "<<SmartFocusOut>>"

    def __init__(self : T | Self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._was_above = None
        self._was_focused = None
        self.bind_all("<Motion>", self._dispatch_event, "+")
        self.bind_all("<Button>", self._dispatch_event, "+")
        self.bind_all("<FocusIn>", self._dispatch_event, "+")

    def _is_inside(self, widget : Widget) -> bool:
        if not isinstance(widget, Widget) : return false
        try :
            while widget:
                if widget == self:
                    return True
                #
                widget = widget.master
            return False
        except KeyError :
            return False

    def get_widget_under_mouse(self : T) :
        x, y = self.winfo_pointerxy()
        return self.winfo_containing(x, y)


    def _dispatch_event(self, event):
        """
        Call the callback of this event
        :param event: The caught event
        :return: None
        """
        match event.type:
            case EventType.Motion:
                self._on_mouse_move(event)

            case EventType.ButtonPress:
                self._on_mouse_clicked(event)

            case EventType.FocusIn:
                self._on_focus_in(event)

            case _:
                pass

    def _on_mouse_move(self : T | Self, event : Event):
        is_above = self._is_inside(event.widget)

        if self._was_above == is_above:
            if is_above : self.event_generate(self.SMART_MOTION)
            return
        #
        self._was_above = is_above
        if is_above:
            self.event_generate(self.SMART_ENTER)
        else:
            self.event_generate(self.SMART_LEAVE)


    def _on_mouse_clicked(self : T | Self, event : Event):
        is_above = self._is_inside(event.widget)
        #If the event is not above me, return
        if not is_above:
            return
        #Call the correct mouse event
        self.event_generate(self.SMART_CLICK)
        match event.num:
            case 1: self.event_generate(self.SMART_L_CLICK)
            case 2: self.event_generate(self.SMART_C_CLICK)
            case 3: self.event_generate(self.SMART_R_CLICK)
            case _: pass

    def _on_focus_in(self : T |Self, event : Event):
        if not self._was_focused and self._is_inside(event.widget) :
            self.event_generate(self.SMART_FOCUS_IN)
            self._was_focused = True
        elif self._was_focused and not self._is_inside(event.widget):
            self._was_focused = False
            self.event_generate(self.SMART_FOCUS_OUT)



############################################################
#                          TEST                            #
############################################################

class CustomCard(SmartEventMixin, Frame):
    def __init__(self, master, title: str, color: str, **kwargs):
        super().__init__(master, **kwargs)
        self.config(bg=color, bd=2, relief="raised")

        # Titre
        self.title_label = Label(self, text=title, bg=color, font=("Arial", 14, "bold"))
        self.title_label.pack(pady=10, padx=10)
        self.entry = Entry(self)
        self.entry.pack()

        # Un bouton interne
        self.action_btn = Button(self, text="Action", command=self.on_button_click)
        self.action_btn.pack(pady=5)

        # Bind SMART events
        self.bind(self.SMART_ENTER, self.on_smart_enter)
        self.bind(self.SMART_LEAVE, self.on_smart_leave)
        self.bind(self.SMART_L_CLICK, self.on_smart_click)
        self.bind(self.SMART_MOTION, self.on_smart_motion)
        self.bind(self.SMART_FOCUS_IN, self.on_smart_in)
        self.bind(self.SMART_FOCUS_OUT, self.on_smart_out)

    # Callbacks SMART
    def on_smart_enter(self, _):
        self.config(relief="solid")
        print(f"{self.title_label['text']} - Mouse Enter")

    def on_smart_leave(self, _):
        self.config(relief="raised")
        print(f"{self.title_label['text']} - Mouse Leave")

    def on_smart_click(self, _):
        print(f"{self.title_label['text']} - Smart Click detected!")

    def on_smart_motion(self, _):
        # Optionnel : print ou update visuel
        pass

    def on_button_click(self):
        print(f"{self.title_label['text']} - Button clicked")

    def on_smart_in(self, _):
        print(f"{self.title_label['text']} - Smart FocusIn detected!")

    def on_smart_out(self, _):
        print(f"{self.title_label['text']} - Smart FocusOut detected!")

if __name__ == "__main__":
    root = Tk()
    root.title("Custom Widget avec SmartEventMixin")
    root.minsize(400, 300)

    card1 = CustomCard(root, "Card Rouge", "red")
    card2 = CustomCard(root, "Card Bleue", "blue")
    card1.pack(pady=10, padx=10, fill="x")
    card2.pack(pady=10, padx=10, fill="x")

    root.mainloop()

