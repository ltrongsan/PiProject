import socket
import sys
import numpy
import time
import pickle
from threading import Thread


class MyServer(Thread):
    """

    """
    def __init__(self, host, port):
        Thread.__init__(self)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)     # create an INET, STREAMing socket

        self.buffer_size = 1024
        self.file_size = 0
        self.send_message = None
        self.receive_message = None

        self.fft_result = None
        self.spectral_sum = None

        self.client_tree = None
        self.client_dict = {}
        self.thread_id = 1
        self.loudspeaker_client_dict = {}
        self.mic_client_dict = {}
        self.camera_client_dict = {}

        self.connection_dict = {}
        self.thread_list = []
        self.server_client_connection = ServerClientConnection(None, None)

        print('Socket created')

        # Bind socket to host and port
        try:
            self.socket.bind((host, port))
        except socket.error as msg:
            print('Bind failed. Error Code : ' + str(msg))
            sys.exit()
        print('Socket bind complete')

        # Start listening on socket
        self.socket.listen(5)
        print('Socket now listening')

    def run(self):
        while 1:
            # wait to accept a connection - blocking call
            self.server_client_connection.connection, \
                self.server_client_connection.address = self.socket.accept()
            self.connection_dict[self.thread_id] = self.server_client_connection.connection

            client_type = self.connection_dict[self.thread_id].recv(1024)
            client_type = client_type.decode()
            print(client_type)
            self.client_dict[self.thread_id] = [self.server_client_connection.address[0],
                                                self.server_client_connection.address[1],
                                                client_type]
            if client_type == "MICROPHONE":
                self.mic_client_dict[self.thread_id] = [self.server_client_connection.address[0],
                                                        self.server_client_connection.address[1],
                                                        client_type]
            elif client_type == "LOUDSPEAKER":
                self.loudspeaker_client_dict[self.thread_id] = [self.server_client_connection.address[0],
                                                                self.server_client_connection.address[1],
                                                                client_type]
            else:
                self.camera_client_dict[self.thread_id] = [self.server_client_connection.address[0],
                                                           self.server_client_connection.address[1],
                                                           client_type]
            print('Connected with IP ' + self.server_client_connection.address[0] + ' port '
                  + str(self.server_client_connection.address[1]))

            new_thread = ClientConnectionThread(self.server_client_connection, self.thread_id)
            self.client_tree.insert("", "end", text=self.thread_id,
                                    values=(self.client_dict[self.thread_id]))
            new_thread.daemon = True
            new_thread.start()
            self.thread_list.append(new_thread)
            self.thread_id = self.thread_id + 1

    def send_command(self, connection, command):
        """

        :param connection:
        :param command:
        :return:
        """
        self.send_message = command
        connection.send(self.send_message.encode())
        time.sleep(1)

    def send_song(self, file_name, connection, isTrue):
        """

        :param file_name:
        :param connection:
        :param isTrue:
        :return:
        """
        buffer_size = 4096
        if isTrue:
            self.send_command(connection, 'CONFIGURE TRUE')
        else:
            self.send_command(connection, 'CONFIGURE FALSE')

        file = open(file_name, 'rb')

        # Send audio file segment
        print('Sending...')
        self.file_size = 0
        data = file.read(buffer_size)
        self.send_message = data

        while data:
            print('Sending...')
            connection.send(self.send_message)
            data = file.read(buffer_size)
            self.send_message = data
            self.file_size += buffer_size

        self.send_message = 'DONE'
        print(self.send_message.encode())
        connection.send(self.send_message.encode())
        print("Done Sending")

    def send_fft_spectral_sum(self, connection):
        """

        :param connection:
        :return:
        """
        pass

    def receive_record_file(self, connection):
        """

        :param connection:
        :return:
        """
        file = open('test.wav', 'wb')
        self.receive_message = connection.recv(self.buffer_size)
        file.write(self.receive_message)
        self.file_size = self.buffer_size
        while self.receive_message:
            print("Receiving...")
            file.write(self.receive_message)
            self.receive_message = connection.recv(self.buffer_size)
            self.file_size += self.buffer_size
        file.close()

    def receive_fft(self, connection):
        """

        :param connection:
        :return:
        """
        buffer_size = 4096
        self.send_command(connection, "GET FFT")
        self.receive_message = connection.recv(buffer_size)
        obj_size = int(self.receive_message)
        self.receive_message = connection.recv(buffer_size)
        serialized = bytearray(self.receive_message)
        recv_size = len(self.receive_message)

        while recv_size < obj_size:
            print("Receiving")
            self.receive_message = connection.recv(buffer_size)
            serialized.extend(self.receive_message)
            recv_size += len(self.receive_message)
        self.fft_result = pickle.loads(serialized)

    def receive_streaming_video(self, conn):
        pass

    def calculate_fft_spectral_sum(self):
        """

        :return:
        """
        self.fft_result = self.fft_result / max(self.fft_result)
        self.spectral_sum = numpy.sum(self.fft_result)

    def plot_fft(self, fft):
        pass

    def show_streaming_video(self):
        pass


class ServerClientConnection:
    def __init__(self, connection, address):
        self.connection = connection
        self.address = address


class ClientConnectionThread(Thread):
    """

    """
    def __init__(self, server_client_conn, client_ID):
        Thread.__init__(self)
        self.connection = server_client_conn.connection
        self.client_IP = server_client_conn.address[0]
        self.client_port = server_client_conn.address[1]
        self.client_ID = client_ID
        print('New connection added: ' + self.client_IP)
        print('Thread number: ' + str(self.client_ID) + '\n')

    def run(self):
        while 1:
            pass

