import socket
import time
import threading
import os
from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
from server_part import server
from server_part import threads


class MyProgram:
    def __init__(self, master):

        self.master = master
        record_frame = Frame(self.master)
        record_frame.grid(row=0, column=0)
        camera_frame = Frame(self.master)
        camera_frame.grid(row=0, column=1)
        configuration_frame = Frame(self.master)
        configuration_frame.grid(row=1, column=0)
        loudspeaker_frame = Frame(self.master)
        loudspeaker_frame.grid(row=1, column=1)

        self.host = socket.gethostname()
        self.port = 8888
        self.threshold = 300

        self.sound_file = None
        self.win = None
        self.stop_record = False

        self.client_tree = Treeview(record_frame)
        self.server1 = server.MyServer(self.host, self.port)
        self.server_thread = threads.ServerThread(self.server1, self.client_tree)
        self.server_thread.start()

        # region Create Table of Clients

        subtitle_text = StringVar()
        subtitle_text.set("MAIN PROGRAM")
        subtitle = Label(self.master, textvariable=subtitle_text)
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
        self.client_tree.grid(row=1, column=1)
        # endregion

        # region Create Buttons

        record_button = Button(configuration_frame, text="RECORD", command=self.thread_record_button)
        record_button.grid(row=1, column=0)
        close_button = Button(configuration_frame, text="CLOSE", command=self.onExit)
        close_button.grid(row=2, column=0)

        configure_true_sound_button = Button(configuration_frame, text="CONFIGURE TRUE SOUND",
                                             command=self.onConfigureTrueSound)
        configure_true_sound_button.grid(row=1, column=2, sticky=W)
        configure_false_sound_button = Button(configuration_frame, text="CONFIGURE FALSE SOUND",
                                              command=self.onConfigureFalseSound)
        configure_false_sound_button.grid(row=2, column=2, sticky=W)

        play_true_sound_button = Button(loudspeaker_frame, text="PLAY TRUE SOUND",
                                        command=self.onPlayTrueSound)
        play_true_sound_button.grid(row=0, column=0, sticky=W)
        play_false_sound_button = Button(loudspeaker_frame, text="PLAY FALSE SOUND",
                                         command=self.onPlayFalseSound)
        play_false_sound_button.grid(row=1, column=0, sticky=W)
        stop_button = Button(loudspeaker_frame, text="STOP", command=self.onStop)
        stop_button.grid(row=2, column=0, sticky=W)

        # endregion

    def open_file(self):
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            name = filedialog.askopenfilename(initialdir=current_dir,
                                              filetypes=(("Mp3 Files", "*.mp3"), ("All Files", "*.*")),
                                              title="Choose a file.")
            if name != '':
                print(name)
                self.sound_file = name
        except:
            print("No file exists")

    def onConfigureTrueSound(self):
        self.open_file()
        if self.sound_file is not None:
            for client_id in self.server_thread.loudspeaker_client_list:
                conn_2 = self.server_thread.connection_dict[client_id]
                self.server1.send_command(conn_2, 'CONFIGURE TRUE')
                self.server1.send_song(self.sound_file, conn_2, 'TRUE')
                self.server1.send_message = None

    def onConfigureFalseSound(self):
        self.open_file()
        if self.sound_file is not None:
            for client_id in self.server_thread.loudspeaker_client_list:
                conn_2 = self.server_thread.connection_dict[client_id]
                self.server1.send_command(conn_2, 'CONFIGURE FALSE')
                self.server1.send_song(self.sound_file, conn_2, 'FALSE')
                self.server1.send_message = None

    def onPlayTrueSound(self):
        for client_id in self.server_thread.loudspeaker_client_list:
            conn_2 = self.server_thread.connection_dict[client_id]
            self.server1.send_command(conn_2, 'PLAY TRUE')
            self.server1.send_message = None

    def onPlayFalseSound(self):
        for client_id in self.server_thread.loudspeaker_client_list:
            conn_2 = self.server_thread.connection_dict[client_id]
            self.server1.send_command(conn_2, 'PLAY FALSE')
            self.server1.send_message = None

    def onStop(self):
        for client_id in self.server_thread.loudspeaker_client_list:
            conn_2 = self.server_thread.connection_dict[client_id]
            self.server1.send_command(conn_2, 'STOP')
            self.server1.send_message = None

    def thread_record_button(self):
        th_record = threading.Thread(target=self.onRecord, args=[])
        th_record.start()

    def onRecord(self):
        self.win = Toplevel()         # create child window
        frame = Frame(self.win)
        frame.pack()

        scrollbar = Scrollbar(frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        listbox = Listbox(frame, width=150, yscrollcommand=scrollbar.set)
        listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)
        Button(self.win, text='Close', command=lambda: self.onClose(conn)).pack(side=BOTTOM)

        for item in self.client_tree.selection():
            client_id = self.client_tree.item(item, 'text')
            conn = self.server_thread.connection_dict[client_id]
            print(client_id)
            listbox.insert(END, client_id)
            print(conn)
            listbox.insert(END, conn)
            listbox.pack(side=LEFT, fill=BOTH)

            self.stop_record = False
            self.record(conn, listbox)

    def onClose(self, conn):
        self.stop_record = True
        self.win.destroy()

    def onExit(self):
        for t in self.server_thread.threads_list:
            t.join()
        print('Exiting')
        self.master.destroy()

    def record(self, conn, listbox):
        while not self.stop_record:
            self.server1.send_command(conn, 'RECORD')
            self.server1.receive_fft(conn)
            print(self.server1.fft_result)
            self.server1.calculate_fft_spectral_sum()
            self.server1.spectral_sum = float(self.server1.spectral_sum)
            message = 'The sum of FFT is : {0:.3f}'.format(self.server1.spectral_sum)
            listbox.insert(END, message)

            for client_id in self.server_thread.loudspeaker_client_list:
                conn_2 = self.server_thread.connection_dict[client_id]
                if self.server1.spectral_sum >= self.threshold:
                    self.server1.send_command(conn_2, 'TRUE')
                elif self.server1.spectral_sum < self.threshold:
                    self.server1.send_command(conn_2, 'FALSE')

            time.sleep(5)


if __name__ == "__main__":
    root = Tk()
    MainProgram = MyProgram(root)
    root.title("MAIN PROGRAM")
    root.mainloop()


