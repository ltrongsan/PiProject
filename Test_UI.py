from tkinter import *
from tkinter.ttk import *


class TestUI(Frame):
    def __init__(self, master):
        self.master = master
        Frame.__init__(self, master)
        self.grid()
        master.title("MAIN PROGRAM")

        self.subtitle_text = StringVar()
        self.subtitle_text.set("MAIN PROGRAM")
        self.subtitle = Label(self.master, textvariable=self.subtitle_text)
        self.subtitle.grid(row=0, sticky=N)

        # self.IP_title_text = StringVar()
        # self.IP_title_text.set("IP")
        # self.IP_title = Label(self.master, textvariable=self.IP_title_text)
        # self.IP_title.grid(row=2, column=0)
        #
        # self.Port_title_text = StringVar()
        # self.Port_title_text.set("Port")
        # self.Port_title = Label(self.master, textvariable=self.Port_title_text)
        # self.Port_title.grid(row=2, column=1)

        client_list = {1: ['192.168.0.1', '6686'],
                       2: ['192.168.1.2', '6996'],
                       3: ['192.172.0.3', '6768']}

        client_tree = Treeview(self.master)
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

        self.record_button = Button(master, text="RECORD", command=self.greet)
        self.record_button.grid(row=1, column=5)

        self.close_button = Button(master, text="CLOSE", command=self.master.quit)
        self.close_button.grid(row=3, column=5)

    def greet(self):
        print("Greetings!")


root = Tk()
my_gui = TestUI(root)
root.mainloop()