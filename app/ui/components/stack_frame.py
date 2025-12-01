import tkinter as tk
from tkinter import Frame


class StackFrame(Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.items: dict[str, Frame] = {}

    def show_child(self, tag: str):
        item = self.items.get(tag)
        if item is None:
            print(f"Failed to show the stack item with tag '{tag}'. Tag not found.")
            return
        item.tkraise()

    def add_stack_item(self, tag: str, **kwargs) -> Frame:
        frame = Frame(self, **kwargs)
        self.items[tag] = frame
        frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        return frame

    def remove_child(self, tag: str) -> Frame | None:
        item = self.items.get(tag)
        if item is None:
            print(f"Failed to remove the stack item with tag '{tag}'. Tag not found.")
            return None
        item.place_forget()
        del self.items[tag]
        return item


if __name__ == "__main__" :
    root = tk.Tk()
    root.geometry("400x400")
    stack = StackFrame(root)
    stack.pack(fill="both", expand=True)
    stack.config(bg="red", width=100, height=100)


    page1 = stack.add_stack_item('1')
    page2 = stack.add_stack_item('2')

    page1.config(bg="red")
    page2.config(bg="blue")

    bt1 = tk.Button(page1, text="Je suis la page1", command=lambda : stack.show_child('2'))
    bt2 = tk.Button(page2, text="Je suis la page 2", command=lambda : stack.show_child('1'))

    bt1.pack()
    bt2.pack()



    stack.show_child("1")
    root.mainloop()
