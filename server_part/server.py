import socket
import sys
import numpy
from threading import Thread
from scipy.io import wavfile
from numpy.fft import fft
import time


class MyServer:

    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)     # create an INET, STREAMing socket
        self.receive_message = None
        self.send_message = None
        self.file_size = 0
        self.buffer_size = 1024

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

    def receive_file(self, connection):
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

    def sum_fourier_transform(self):
        rate, sound_data = wavfile.read('test.wav')
        sound_data = sound_data / (2. ** 15)
        fft_result = fft(sound_data)
        fft_length = int(len(fft_result) / 2)
        fft_result = abs(fft_result[0:fft_length - 1])
        fft_result = fft_result / max(fft_result)
        spectral_sum = numpy.sum(fft_result)
        self.send_message = str(spectral_sum)

    def send_record_command(self, connection):
        while 1:
            self.send_message = 'RECORD'
            connection.send(self.send_message.encode())
            time.sleep(10)


class ServerClientConnection:
    def __init__(self, connection, address):
        self.connection = connection
        self.address = address

