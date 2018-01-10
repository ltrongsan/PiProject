import socket
import sys
from threading import Thread
from tkinter import *
from tkinter.ttk import *
from server_part import server


class MyProgram:
    def __init__(self, master):
        self.master = master
        self.client_list = {'1': ['192.168.2.2', '6868']}
        self.threads = []
        self.threads_id = 2
        self.connection = None
        self.address = None
        self.host = socket.gethostname()
        self.port = 8888
        self.buffer_size = 1024
        self.sampling_freq = 44100

        self.server1 = server.MyServer(self.host, self.port)
        self.thread_start_server = Thread(target=self.start_server).start()

        subtitle_text = StringVar()
        subtitle_text.set("MAIN PROGRAM")
        subtitle = Label(master, textvariable=subtitle_text)
        subtitle.grid(row=0, sticky=N)

        self.client_tree = Treeview(master)
        self.client_tree['columns'] = ('ip', 'port', 'status')
        self.client_tree.heading("#0", text='No.')
        self.client_tree.column("#0", anchor='center', width=30)
        self.client_tree.heading('ip', text='IP address')
        self.client_tree.column('ip', anchor='center', width=200)
        self.client_tree.heading('port', text='Port')
        self.client_tree.column('port', anchor='center', width=70)
        self.client_tree.heading('status', text='Status')
        self.client_tree.column('status', anchor='center', width=100)

        for client_address in self.client_list.keys():
            self.client_tree.insert("", "end", text=client_address, values=(self.client_list[client_address]))
        self.client_tree.grid(row=1)

        record_button = Button(master, text="RECORD", command=lambda: self.server1.send_record_command(self.connection))
        record_button.grid(row=1, column=5)

        close_button = Button(master, text="CLOSE", command=self.onExit)
        close_button.grid(row=3, column=5)

    def start_server(self):
        while 1:
            # now keep talking with the client
            # wait to accept a connection - blocking call
            self.connection, self.address = self.server1.socket.accept()
            print('Connected with IP ' + self.address[0] + ' port ' + str(self.address[1]))
            self.client_list[self.threads_id] = [self.address[0], self.address[1]]
            new_thread = server.ClientThread(self.server1, self.connection, self.address, self.threads_id)

            self.client_tree.insert("", "end", text=self.threads_id, values=(self.client_list[self.threads_id]))

            new_thread.run()
            self.threads.append(new_thread)
            self.threads_id = self.threads_id + 1

            self.server1.receive_message = self.connection.recv(self.buffer_size)
            spectral_sum = float(self.server1.receive_message.decode())
            print('The sum of FFT is : {0:.3f}'.format(spectral_sum))

    def onExit(self):
        self.master.destroy()


root = Tk()
MainProgram = MyProgram(root)
root.title("MAIN PROGRAM")
root.mainloop()


