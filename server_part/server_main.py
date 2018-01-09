import socket
import sys
from threading import Thread
from tkinter import *
from tkinter.ttk import *
from server_part import server

root = Tk()


def start_server():
    while 1:
        global connection, threads, threads_id
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

threads = []
threads_id = 1

server1 = server.MyServer(host, port)
thread_start_server = Thread(target=start_server).start()


class MainUI:
    def __init__(self, master):
        master.title("MAIN PROGRAM")

        self.subtitle_text = StringVar()
        self.subtitle_text.set("MAIN PROGRAM")
        self.subtitle = Label(master, textvariable=self.subtitle_text)
        self.subtitle.grid(row=0, sticky=N)

        client_list = {1: ['192.168.0.1', '6686'],
                       2: ['192.168.1.2', '6996'],
                       3: ['192.172.0.3', '6768']}

        client_tree = Treeview(master)
        client_tree['columns'] = ('ip', 'port', 'status')
        client_tree.heading("#0", text='No.')
        client_tree.column("#0", anchor='center', width=30)
        client_tree.heading('ip', text='IP address')
        client_tree.column('ip', anchor='center', width=200)
        client_tree.heading('port', text='Port')
        client_tree.column('port', anchor='center', width=70)
        client_tree.heading('status', text='Status')
        client_tree.column('status', anchor='center', width=100)

        for client_address in client_list.keys():
            client_tree.insert("", "end", text=client_address, values=(client_list[client_address]))
        client_tree.grid(row=1)

        self.record_button = Button(master, text="RECORD", command=server1.send_record_command)
        self.record_button.grid(row=1, column=5)

        self.close_button = Button(master, text="CLOSE", command=onExit)
        self.close_button.grid(row=3, column=5)


def main():
    MainUI(root)
    root.mainloop()


def onExit():
    thread_start_server.join()
    for thread in threads:
        thread.shutdown_flag.set()
        thread.join()
    root.quit()



main()
