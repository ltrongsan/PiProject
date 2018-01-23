from threading import Thread
from server_part import server


class ServerThread(Thread):
    def __init__(self, my_server, client_tree):
        self.client_tree = client_tree
        Thread.__init__(self)
        self.my_server = my_server
        self.threads_id = 2
        self.buffer_size = 1024
        self.sampling_freq = 44100
        self.client_dict = {'1': ['192.168.2.2', '6868']}
        self.threads = []
        self.server_client_connection = server.ServerClientConnection(None, None)
        self.connection_dict = {}

    def run(self):
        while 1:
            # wait to accept a connection - blocking call
            self.server_client_connection.connection, \
                self.server_client_connection.address = self.my_server.socket.accept()
            self.connection_dict[self.threads_id] = self.server_client_connection.connection
            print('Connected with IP ' + self.server_client_connection.address[0] + ' port '
                  + str(self.server_client_connection.address[1]))

            self.client_dict[self.threads_id] = [self.server_client_connection.address[0],
                                                 self.server_client_connection.address[1]]
            new_thread = ClientThread(self.my_server, self.server_client_connection, self.threads_id)
            self.client_tree.insert("", "end", text=self.threads_id, values=(self.client_dict[self.threads_id]))
            new_thread.daemon = True
            new_thread.start()
            self.threads.append(new_thread)
            self.threads_id = self.threads_id + 1

            # self.my_server.receive_message = self.connection.recv(self.buffer_size)
            # spectral_sum = float(self.my_server.receive_message.decode())
            # print('The sum of FFT is : {0:.3f}'.format(spectral_sum))


class ClientThread(Thread):
    def __init__(self, server, server_client_conn, client_ID):
        Thread.__init__(self)
        self.server = server
        self.connection = server_client_conn.connection
        self.client_IP = server_client_conn.address[0]
        self.client_port = server_client_conn.address[1]
        self.client_ID = client_ID
        print('New connection added: ' + self.client_IP)
        print('Thread number: ' + str(self.client_ID) + '\n')

    def run(self):
        global client_tree
        while 1:
            self.server.receive_message = self.connection.recv(1024)  # Receive message
            spectral_sum = float(self.server.receive_message.decode())
            print('The sum of FFT is : {0:.3f}'.format(spectral_sum))