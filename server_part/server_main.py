import socket
import sys
from threading import Thread
from tkinter import *
from tkinter.ttk import *
from server_part import server
from server_part import threads


class MyProgram:
    def __init__(self, master):
        self.master = master
        self.host = socket.gethostname()
        self.port = 8888
        self.client_tree = Treeview(master)

        self.server1 = server.MyServer(self.host, self.port)
        server_thread = threads.ServerThread(self.server1, self.client_tree)
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
        for client_address in server_thread.client_dict.keys():
            self.client_tree.insert("", "end", text=client_address,
                                    values=(server_thread.client_dict[client_address]))
        self.client_tree.grid(row=1)

        record_button = Button(master, text="RECORD",
                               command=lambda:
                               self.server1.send_record_command(server_thread.server_client_connection.connection))
        record_button.grid(row=1, column=5)

        close_button = Button(master, text="CLOSE", command=self.onExit)
        close_button.grid(row=3, column=5)

    def onRecord(self):
        for item in self.client_tree.selection():
            item_text = self.client_tree.item(item, "text")
            print(item_text)

    def onExit(self):
        pass


root = Tk()
MainProgram = MyProgram(root)
root.title("MAIN PROGRAM")
root.mainloop()


