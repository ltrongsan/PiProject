import socket
import threading
import time
from tkinter import *
from server_part import server


def start_server():
    while 1:
        global connection
        # now keep talking with the client
        # wait to accept a connection - blocking call
        connection, address = server1.socket.accept()
        print('Connected with ' + address[0] + ':' + str(address[1]))

        server1.receive_message = connection.recv(buffer_size)  # Receive command message (1st message)
        spectral_sum = float(server1.receive_message.decode())
        print('The sum of FFT is : {0:.3f}'.format(spectral_sum))


def record():
    global connection
    while (1):
        server1.send_message = 'RECORD'
        connection.send(server1.send_message.encode())
        time.sleep(10)


def thread_start_server():
    threading.Thread(target=start_server).start()


host = socket.gethostname()
port = 8888
buffer_size = 1024
sampling_freq = 44100

server1 = server.MyServer(host, port)
thread_start_server()

# create a Record Button
root = Tk()
frame = Frame(root)
frame.pack()
record_button = Button(frame, text="RECORD", bg="red", fg="black", command=record)
record_button.pack(side=RIGHT)

root.mainloop()