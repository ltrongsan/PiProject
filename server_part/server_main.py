import socket
import time
import threading
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
        self.server_thread = threads.ServerThread(self.server1, self.client_tree)
        self.server_thread.start()

        # region Create Table of Clients
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

        for client_address in self.server_thread.client_dict.keys():
            self.client_tree.insert("", "end", text=client_address,
                                    values=(self.server_thread.client_dict[client_address]))
        self.client_tree.grid(row=1)
        # endregion

        # region Create Buttons
        configure_true_sound_button = Button(master, text="CONFIGURE TRUE SOUND",
                                             command=self.onConfigureTrueSound)
        configure_true_sound_button.grid(row=3, column=0, sticky=W)
        configure_false_sound_button = Button(master, text="CONFIGURE FALSE SOUND",
                                              command=self.onConfigureFalseSound)
        configure_false_sound_button.grid(row=4, column=0, sticky=W)
        record_button = Button(master, text="RECORD", command=self.thread_record_button)
        record_button.grid(row=3, column=1)
        close_button = Button(master, text="CLOSE", command=self.onExit)
        close_button.grid(row=4, column=1)
        # endregion

    def onConfigureTrueSound(self):
        pass

    def onConfigureFalseSound(self):
        pass

    def thread_record_button(self):
        th_record = threading.Thread(target=self.onRecord, args=[])
        th_record.start()

    def onRecord(self):
        win = Toplevel()         # create child window
        frame = Frame(win)
        frame.pack()

        scrollbar = Scrollbar(frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        listbox = Listbox(frame, width=150, yscrollcommand=scrollbar.set)
        listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)

        Button(win, text='Close', command=win.destroy).pack(side=BOTTOM)

        # create a client list UI
        for item in self.client_tree.selection():
            client_id = self.client_tree.item(item, 'text')
            conn = self.server_thread.connection_dict[client_id]
            print(client_id)
            listbox.insert(END, client_id)
            print(conn)
            listbox.insert(END, conn)
            listbox.pack(side=LEFT, fill=BOTH)

            self.record(conn, listbox)

        # attach listbox to scrollbar
        listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)

    def onExit(self):
        pass

    def record(self, conn, listbox):
        while 1:
            self.server1.send_command(conn, 'RECORD')
            self.server1.receive_fft(conn)
            print(self.server1.fft_result)
            self.server1.calculate_fft_spectral_sum()
            self.server1.spectral_sum = float(self.server1.spectral_sum)
            message = 'The sum of FFT is : {0:.3f}'.format(self.server1.spectral_sum)
            listbox.insert(END, message)

            for client_id in self.server_thread.loudspeaker_client_list:
                message = str(self.server1.spectral_sum)
                conn_2 = self.server_thread.connection_dict[client_id]
                conn_2.send(message.encode())

            time.sleep(8)


if __name__ == "__main__":
    root = Tk()
    MainProgram = MyProgram(root)
    root.title("MAIN PROGRAM")
    root.mainloop()


