from tkinter import *
import cv2
from PIL import Image, ImageTk

isrunning = 0


def start():
    global isrunning
    if isrunning == 0:
        global cap
        cap = cv2.VideoCapture(0)
        isrunning = 1
        lmain.grid(row = 1,column = 1)

        def show_frame():
            _, frame = cap.read()
            frame = cv2.flip(frame, 1)
            frame = cv2.resize(frame, (800,600))
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            lmain.imgtk = imgtk
            lmain.configure(image=imgtk)
            if isrunning == 1:
                lmain.after(10, show_frame)
            else:
                cap.release()
    show_frame()


def Stop():
    global isrunning
    isrunning = 0
    lmain.grid_forget()

def main():
    Stop()
    #Reset.invoke()
    #stopFunc.invoke()


root = Tk()
lmain = Label(root, width = 800, height = 600, bg = "blue")
stopFunc = Button(root, text = "stop", command = Stop)
Reset = Button(root, text = "Reset", command = start)
Main = Button(root, text = "Stop", command = main)
Start = Button(root, text = "Start", command = start)
Start.grid(row = 0, column = 0)
Main.grid(row = 0, column = 1)

root.mainloop()