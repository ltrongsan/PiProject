import socket
import time
from threading import Thread
from tkinter import *
from server_part import server


def start_server():
    threads = []
    threads_id = 1
    while 1:
        global connection
        # now keep talking with the client
        # wait to accept a connection - blocking call
        connection, address = server1.socket.accept()
        print('Connected with IP ' + address[0] + ' port ' + str(address[1]))
        new_thread = server.ClientThread(server1, connection, address, threads_id)
        new_thread.run()
        threads.append(new_thread)
        threads_id = threads_id + 1

        server1.receive_message = connection.recv(buffer_size)  # Receive command message (1st message)
        spectral_sum = float(server1.receive_message.decode())
        print('The sum of FFT is : {0:.3f}'.format(spectral_sum))


host = socket.gethostname()
port = 8888
buffer_size = 1024
sampling_freq = 44100

server1 = server.MyServer(host, port)
Thread(target=start_server).start()

# create a Record Button
root = Tk()
root.title('Main Program')
frame = Frame(root)
frame.pack()
record_button = Button(frame, text="RECORD",
                       bg="red", fg="black",
                       command=lambda: server1.send_record_command(connection))
record_button.pack(side=RIGHT)

root.mainloop()