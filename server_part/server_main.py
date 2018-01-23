import socket
from tkinter import *
from server_part import server
from server_part import threads
from tkinter.ttk import *


class MyProgram:
    def __init__(self, master):
        global client_tree
        self.master = master
        self.host = socket.gethostname()
        self.port = 8888
        self.server1 = server.MyServer(self.host, self.port)
        new_server_thread = threads.ServerThread(self.server1, client_tree)
        new_server_thread.start()

        subtitle_text = StringVar()
        subtitle_text.set("MAIN PROGRAM")
        subtitle = Label(master, textvariable=subtitle_text)
        subtitle.grid(row=0, sticky=N)

        client_tree['columns'] = ('ip', 'port', 'status')
        client_tree.heading("#0", text='No.')
        client_tree.column("#0", anchor='center', width=30)
        client_tree.heading('ip', text='IP address')
        client_tree.column('ip', anchor='center', width=200)
        client_tree.heading('port', text='Port')
        client_tree.column('port', anchor='center', width=70)
        client_tree.heading('status', text='Status')
        client_tree.column('status', anchor='center', width=100)

        for client_address in new_server_thread.client_dict.keys():
            client_tree.insert("", "end", text=client_address,
                               values=(new_server_thread.client_dict[client_address]))
        client_tree.grid(row=1)

        record_button = Button(master, text="RECORD",
                               command=lambda:
                               self.server1.send_record_command(new_server_thread.server_client_connection.connection))
        record_button.grid(row=1, column=5)

        close_button = Button(master, text="CLOSE", command=self.onExit)
        close_button.grid(row=3, column=5)

    def onExit(self):
        self.master.destroy()


root = Tk()
client_tree = Treeview(root)
MainProgram = MyProgram(root)
root.title("MAIN PROGRAM")
root.mainloop()


