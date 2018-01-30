from tkinter import *


class DebugScrollbar(Scrollbar):
    def set(self, *args):
        print("SCROLLBAR SET", args)
        Scrollbar.set(self, *args)


class DebugListbox(Listbox):
    def yview(self, *args):
        print("LISTBOX YVIEW", args)
        Listbox.yview(self, *args)


scrollbar = DebugScrollbar()
scrollbar.pack(side=RIGHT, fill=Y)

listbox = DebugListbox(yscrollcommand=scrollbar.set)
listbox.pack()

for i in range(100):
    listbox.insert(END, i)

# attach listbox to scrollbar
listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

mainloop()