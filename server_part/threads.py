from threading import Thread
from server_part import server


class ServerThread(Thread):
    def __init__(self, my_server, client_tree):
        self.client_tree = client_tree
        Thread.__init__(self)
        self.my_server = my_server
        self.threads_id = 1

        self.client_dict = {}
        self.mic_client_list = []
        self.loudspeaker_client_list = []

        self.threads = []
        self.server_client_connection = server.ServerClientConnection(None, None)
        self.connection_dict = {}

    def run(self):
        while 1:
            # wait to accept a connection - blocking call
            self.server_client_connection.connection, \
                self.server_client_connection.address = self.my_server.socket.accept()
            self.connection_dict[self.threads_id] = self.server_client_connection.connection

            client_type = self.connection_dict[self.threads_id].recv(1024)
            client_type = client_type.decode()
            print(client_type)
            if client_type == "MICROPHONE":
                self.mic_client_list.append(self.threads_id)
            else:
                self.loudspeaker_client_list.append(self.threads_id)

            self.client_dict[self.threads_id] = [self.server_client_connection.address[0],
                                                 self.server_client_connection.address[1],
                                                 client_type]
            print('Connected with IP ' + self.server_client_connection.address[0] + ' port '
                  + str(self.server_client_connection.address[1]))

            new_thread = ClientThread(self.my_server, self.server_client_connection, self.threads_id)
            self.client_tree.insert("", "end", text=self.threads_id,
                                    values=(self.client_dict[self.threads_id]))
            new_thread.daemon = True
            new_thread.start()
            self.threads.append(new_thread)
            self.threads_id = self.threads_id + 1


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
        while 1:
            pass