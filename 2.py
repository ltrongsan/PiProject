# display message in a child window
from tkinter import *


def messageWindow():
    # create child window
    win = Toplevel()
    # display message
    message = "This is the child window"
    Label(win, text=message).pack()
    # quit child window and return to root window
    # the button is optional here, simply use the corner x of the child window
    Button(win, text='OK', command=win.destroy).pack()


# create root window
root = Tk()
# put a button on it, or a menu
Button(root, text='Bring up Message', command=messageWindow).pack()
# start event-loop
root.mainloop()
