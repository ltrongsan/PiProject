import socket
import sys
import numpy
import time
import pickle
import cv2
from threading import Thread


class MyServer(Thread):
    """

    """
    def __init__(self, host, port):
        Thread.__init__(self)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)     # create an INET, STREAMing socket

        self.BUFFER_SIZE = 4096
        self.file_size = 0
        self.send_message = None
        self.receive_message = None

        self.fft_result = None
        self.spectral_sum = None
        self.img = None

        self.client_tree = None
        self.client_dict = {}
        self.loudspeaker_client_dict = {}
        self.mic_client_dict = {}
        self.camera_client_dict = {}
        self.disconnected_client_key_list = []

        self.connection_dict = {}
        self.thread_list = []

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
            server_client_connection = ServerClientConnection(None, None)
            server_client_connection.connection, \
                server_client_connection.address = self.socket.accept()
            self.client_tree.delete(*self.client_tree.get_children())
            self.check_connection_dict()
            self.update_connection_dict()
            thread_id = 1
            value = self.connection_dict.get(thread_id)
            while value is not None:
                thread_id += 1
                value = self.connection_dict.get(thread_id)
            self.connection_dict[thread_id] = server_client_connection.connection
            client_type = self.connection_dict[thread_id].recv(1024)
            client_type = client_type.decode()
            print('\n' + client_type)
            self.client_dict[thread_id] = [server_client_connection.address[0],
                                           server_client_connection.address[1],
                                           client_type]
            if client_type == "MICROPHONE":
                self.mic_client_dict[thread_id] = [server_client_connection.address[0],
                                                   server_client_connection.address[1],
                                                   client_type]
            elif client_type == "LOUDSPEAKER":
                self.loudspeaker_client_dict[thread_id] = [server_client_connection.address[0],
                                                           server_client_connection.address[1],
                                                           client_type]
            else:
                self.camera_client_dict[thread_id] = [server_client_connection.address[0],
                                                      server_client_connection.address[1],
                                                      client_type]
            print('Connected with IP ' + server_client_connection.address[0] + ' port '
                  + str(server_client_connection.address[1]))
            for connection_id in self.connection_dict:
                self.client_tree.insert("", "end", text=connection_id,
                                        values=(self.client_dict[connection_id]))

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
        if isTrue:
            self.send_command(connection, 'CONFIGURE TRUE')
        else:
            self.send_command(connection, 'CONFIGURE FALSE')

        file = open(file_name, 'rb')

        # Send audio file segment
        print('Sending...')
        self.file_size = 0
        data = file.read(self.BUFFER_SIZE)
        self.send_message = data

        while data:
            print('Sending...')
            connection.send(self.send_message)
            data = file.read(self.BUFFER_SIZE)
            self.send_message = data
            self.file_size += self.BUFFER_SIZE

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
        self.receive_message = connection.recv(self.BUFFER_SIZE)
        file.write(self.receive_message)
        self.file_size = self.BUFFER_SIZE
        while self.receive_message:
            print("Receiving...")
            file.write(self.receive_message)
            self.receive_message = connection.recv(self.BUFFER_SIZE)
            self.file_size += self.BUFFER_SIZE
        file.close()

    def receive_fft(self, connection):
        """

        :param connection:
        :return:
        """
        self.send_command(connection, "GET FFT")
        self.receive_message = connection.recv(self.BUFFER_SIZE)
        obj_size = int(self.receive_message)
        self.receive_message = connection.recv(self.BUFFER_SIZE)
        serialized = bytearray(self.receive_message)
        recv_size = len(self.receive_message)

        while recv_size < obj_size:
            print("Receiving")
            self.receive_message = connection.recv(self.BUFFER_SIZE)
            serialized.extend(self.receive_message)
            recv_size += len(self.receive_message)
        self.fft_result = pickle.loads(serialized)

    def receive_streaming_video(self, conn):
        self.receive_message = conn.recv(self.BUFFER_SIZE)
        nparr = numpy.fromstring(self.receive_message, numpy.uint8)
        self.img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    def calculate_fft_spectral_sum(self):
        """

        :return:
        """
        self.fft_result = self.fft_result / max(self.fft_result)
        self.spectral_sum = numpy.sum(self.fft_result)

    def plot_fft(self, fft):
        pass

    def check_connection_dict(self):
        for connection_id in self.connection_dict:
            try:
                self.connection_dict[connection_id].send(b'test')
            except:
                self.disconnected_client_key_list.append(connection_id)
                continue

    def update_connection_dict(self):
        for connection_id in self.disconnected_client_key_list:
            client_type = self.client_dict[connection_id][2]
            if client_type == "MICROPHONE":
                del self.mic_client_dict[connection_id]
            elif client_type == "LOUDSPEAKER":
                del self.loudspeaker_client_dict[connection_id]
            else:
                del self.camera_client_dict[connection_id]
            del self.client_dict[connection_id]
            del self.connection_dict[connection_id]

    def show_streaming_video(self, conn):
        self.receive_message(conn)
        if type(self.img) is type(None):
            pass
        else:
            try:
                cv2.imshow('MyCam', self.img)
            except:
                exit(0)

    def capture_video(self):
        cam = cv2.VideoCapture(0)
        while True:
            ret_val, self.img = cam.read()
            self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGBA)


class ServerClientConnection:
    def __init__(self, connection, address):
        self.connection = connection
        self.address = address

