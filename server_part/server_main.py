import socket
import threading
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
        if server1.receive_message.decode() == 'SEND':          # Handle 'SEND' command
            while server1.is_receiving_mess():
                print("Receiving...")
                server1.receive(connection)
                print("Done Receiving")
        elif server1.receive_message.decode() == 'RECEIVE':     # Handle 'RECEIVE' command
            server1.sum_fourier_transform()                     # Process FFT
            connection.send(server1.send_message.encode())      # Send result (sum of FFT spectral)


def record():
    global connection
    server1.send_message = 'RECORD'
    connection.send(server1.send_message.encode())


def threadStartServer():
    threading.Thread(target=start_server).start()


# def threadRecord():
#     threading.Thread(target=record).start()


host = socket.gethostname()
port = 8888
buffer_size = 1024
sampling_freq = 44100

server1 = server.MyServer(host, port)

root = Tk()
frame = Frame(root)
frame.pack()

# start_button = Button(frame, text="START SERVER", fg="black", command=threadStart)
# start_button.pack(side=LEFT)

threadStartServer()

record_button = Button(frame, text="RECORD", bg="red", fg="black", command=record)
record_button.pack(side=RIGHT)

root.mainloop()