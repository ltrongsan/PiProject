import socket
import sys
from threading import Thread
from tkinter import *
from tkinter.ttk import *
from server_part import server
from server_part import threads


class ServerThread(Thread):

    def __init__(self, my_server, client_tree):
        Thread.__init__(self)
        self.my_server = my_server
        self.client_tree = client_tree
        self.threads_id = 2
        self.buffer_size = 1024
        self.sampling_freq = 44100

        self.client_list = {'1': ['192.168.2.2', '6868']}
        self.threads = []

        self.server_client_connection = server.ServerClientConnection(None, None)

    def run(self):
        while 1:
            # wait to accept a connection - blocking call
            self.server_client_connection.connection, \
                self.server_client_connection.address = self.my_server.socket.accept()
            print('Connected with IP ' + self.server_client_connection.address[0] + ' port '
                  + str(self.server_client_connection.address[1]))

            self.client_list[self.threads_id] = [self.server_client_connection.address[0],
                                                 self.server_client_connection.address[1]]
            new_thread = threads.ClientThread(self.my_server, self.server_client_connection, self.threads_id)
            self.client_tree.insert("", "end", text=self.threads_id, values=(self.client_list[self.threads_id]))
            new_thread.daemon = True
            new_thread.start()
            self.threads.append(new_thread)
            self.threads_id = self.threads_id + 1

            # self.my_server.receive_message = self.connection.recv(self.buffer_size)
            # spectral_sum = float(self.my_server.receive_message.decode())
            # print('The sum of FFT is : {0:.3f}'.format(spectral_sum))


class MyProgram:
    def __init__(self, master):
        self.master = master
        self.host = socket.gethostname()
        self.port = 8888
        self.client_tree = Treeview(master)

        self.server1 = server.MyServer(self.host, self.port)
        server_thread = ServerThread(self.server1, self.client_tree)
        server_thread.start()

        subtitle_text = StringVar()
        subtitle_text.set("MAIN PROGRAM")
        subtitle = Label(master, textvariable=subtitle_text)
        subtitle.grid(row=0, sticky=N)

        self.client_tree['columns'] = ('ip', 'port', 'status')
        self.client_tree.heading("#0", text='No.')
        self.client_tree.column("#0", anchor='center', width=30)
        self.client_tree.heading('ip', text='IP address')
        self.client_tree.column('ip', anchor='center', width=200)
        self.client_tree.heading('port', text='Port')
        self.client_tree.column('port', anchor='center', width=70)
        self.client_tree.heading('status', text='Status')
        self.client_tree.column('status', anchor='center', width=100)

        for client_address in server_thread.client_list.keys():
            self.client_tree.insert("", "end", text=client_address,
                                    values=(server_thread.client_list[client_address]))
        self.client_tree.grid(row=1)

        record_button = Button(master, text="RECORD",
                               command=lambda:
                               self.server1.send_record_command(server_thread.server_client_connection.connection))
        record_button.grid(row=1, column=5)

        close_button = Button(master, text="CLOSE", command=self.onExit)
        close_button.grid(row=3, column=5)

    def onExit(self):
        self.master.destroy()


root = Tk()
MainProgram = MyProgram(root)
root.title("MAIN PROGRAM")
root.mainloop()


