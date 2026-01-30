import tkinter
from tkinter import Widget, Event, EventType, Label, Tk, Frame, Button


class SmartEventMixin:

    SMART_ENTER = "<<SmartEnter>>"
    SMART_LEAVE = "<<SmartLeave>>"
    SMART_L_CLICK = "<<SmartLClick>>"
    SMART_R_CLICK = "<<SmartRClick>>"
    SMART_C_CLICK = "<<SmartCClick>>"
    SMART_MOTION = "<<SmartMotion>>"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._was_above = None
        self.bind_all("<Motion>", self._dispatch_event, "+")
        self.bind_all("<Button>", self._dispatch_event, "+")

    def _is_inside(self, widget : Widget) -> bool:
        while widget:
            if widget == self:
                return True
            widget = widget.master
        return False

    def _mouse_is_above(self) -> bool:
        """
        Check if the mouse is above this widget
        :return: True if the mouse is above, False otherwise
        """
        x, y = self.winfo_pointerxy()
        widget = self.winfo_containing(x, y)
        #
        return self._is_inside(widget)

    def _dispatch_event(self, event):
        """
        Call the callback of this event
        :param event: The catched event
        :return: None
        """
        match event.type:
            case EventType.Motion:
                self._on_mouse_move(event)

            case EventType.ButtonPress:
                self._on_mouse_clicked(event)

            case _:
                pass

    def _on_mouse_move(self, event : Event):
        is_above = self._mouse_is_above()

        if self._was_above == is_above:
            if is_above : self.event_generate(self.SMART_MOTION)
            return
        #
        self._was_above = is_above
        if is_above:
            self.event_generate(self.SMART_ENTER)
            self.after(3000, self._on_mouse_move, None)
        else:
            self.event_generate(self.SMART_LEAVE)


    def _on_mouse_clicked(self, event : Event):
        is_above = self._mouse_is_above()
        #If the event is not above me, return
        if not is_above:
            return
        #Call the correct mouse event
        match event.num:
            case 1: self.event_generate(self.SMART_L_CLICK)
            case 2: self.event_generate(self.SMART_C_CLICK)
            case 3: self.event_generate(self.SMART_R_CLICK)
            case _: pass


class CustomCard(SmartEventMixin, Frame):
    def __init__(self, master, title: str, color: str, **kwargs):
        super().__init__(master, **kwargs)
        self.config(bg=color, bd=2, relief="raised")

        # Titre
        self.title_label = Label(self, text=title, bg=color, font=("Arial", 14, "bold"))
        self.title_label.pack(pady=10, padx=10)

        # Un bouton interne
        self.action_btn = Button(self, text="Action", command=self.on_button_click)
        self.action_btn.pack(pady=5)

        # Bind SMART events
        self.bind(self.SMART_ENTER, self.on_smart_enter)
        self.bind(self.SMART_LEAVE, self.on_smart_leave)
        self.bind(self.SMART_L_CLICK, self.on_smart_click)
        self.bind(self.SMART_MOTION, self.on_smart_motion)

    # Callbacks SMART
    def on_smart_enter(self, event):
        self.config(relief="solid")
        print(f"{self.title_label['text']} - Mouse Enter")

    def on_smart_leave(self, event):
        self.config(relief="raised")
        print(f"{self.title_label['text']} - Mouse Leave")

    def on_smart_click(self, event):
        print(f"{self.title_label['text']} - Smart Click detected!")

    def on_smart_motion(self, event):
        # Optionnel : print ou update visuel
        pass

    def on_button_click(self):
        print(f"{self.title_label['text']} - Button clicked")

if __name__ == "__main__":
    root = Tk()
    root.title("Custom Widget avec SmartEventMixin")
    root.minsize(400, 300)

    card1 = CustomCard(root, "Card Rouge", "red")
    card2 = CustomCard(root, "Card Bleue", "blue")
    card1.pack(pady=10, padx=10, fill="x")
    card2.pack(pady=10, padx=10, fill="x")

    root.mainloop()

