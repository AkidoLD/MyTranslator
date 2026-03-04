import tkinter
from tkinter.ttk import Style, Entry

root = tkinter.Tk()
root.geometry("500x400")
s = Style()

# Voir les éléments qui composent un widget
print(s.layout("TEntry"))

# Voir les propriétés configurables d'un élément
print(s.element_options("TEntry.padding"))
print(s.element_options("TEntry.field"))
print(s.element_options("TEntry.textarea"))

s.configure(
    "Custom.TEntry",
    font=("Ubuntu", 16),
    shiftrelief=10,
    width=100
)
s.layout("Custom.TEntry", [
    ("Entry.padding", {"sticky": "nswe", "children": [
        ("Entry.textarea", {"sticky": "nswe"})
    ]})
])
print(s.lookup("Custom.TEntry", "font"))

# Ou pour l'élément interne
print(s.lookup("Entry.textarea", "font"))
print(s.lookup("Entry.textarea", "width"))

entry = Entry(root, style="Custom.TEntry")
entry.pack(side="top", fill='x')

root.mainloop()