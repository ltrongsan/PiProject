import socket
import sys
import numpy
import time
import pickle


class MyServer:
    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)     # create an INET, STREAMing socket
        self.receive_message = None
        self.send_message = None
        self.file_size = 0
        self.buffer_size = 1024

        self.spectral_sum = None
        self.fft_result = None

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

    def send_command(self, connection, command):
        self.send_message = command
        connection.send(self.send_message.encode())
        time.sleep(1)

    def send_song(self, connection, isTrue):
        buffer_size = 2048
        if isTrue:
            self.send_command(connection, 'CONFIGURE TRUE')
        else:
            self.send_command(connection, 'CONFIGURE FALSE')

        # Send audio file segment
        print('Sending...')
        self.file_size = buffer_size
        data = file.read(buffer_size)
        self.send_message = data
        while data:
            print('Sending...')
            self.socket.send(self.send_message)
            data = file.read(buffer_size)
            self.send_message = data
            self.file_size += buffer_size
        print("Done Sending")

    def send_fft_spectral_sum(self, connection):
        pass

    def receive_record_file(self, connection):
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
        buffer_size = 4096
        self.send_command(connection, "GET FFT")
        self.receive_message = connection.recv(buffer_size)
        obj_size = int(self.receive_message)
        self.receive_message = connection.recv(buffer_size)
        serialized = bytearray(self.receive_message)
        rev_size = len(self.receive_message)
        while rev_size < obj_size:
            print("Receiving")
            self.receive_message = connection.recv(buffer_size)
            serialized.extend(self.receive_message)
            rev_size += len(self.receive_message)
        self.fft_result = pickle.loads(serialized)

    def calculate_fft_spectral_sum(self):
        self.fft_result = self.fft_result / max(self.fft_result)
        self.spectral_sum = numpy.sum(self.fft_result)

    def plot_fft(self, fft):
        pass


class ServerClientConnection:
    def __init__(self, connection, address):
        self.connection = connection
        self.address = address

