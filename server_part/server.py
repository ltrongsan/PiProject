import socket
import sys
import numpy
import time
import pickle
import matplotlib.pyplot as plt
from scipy.io import wavfile
from numpy.fft import fft


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

    def send_command(self, connection, command):
        self.send_message = command
        connection.send(self.send_message.encode())
        time.sleep(1)

    def receive_fft(self, connection):
        self.receive_message = connection.recv(self.buffer_size)
        self.receive_message = connection.recv(self.buffer_size)
        serialized = bytearray(self.receive_message)
        print(serialized)
        while self.receive_message:
            print("Receiving")
            serialized.extend(self.receive_message)
            self.receive_message = connection.recv(self.buffer_size)
            print(len(serialized))
        print("Done Receiving")
        print(serialized)
        self.fft_result = pickle.loads(serialized)

    def send_fft_spectral_sum(self, connection):
        pass

    def sum_fourier_transform(self):
        rate, sound_data = wavfile.read('test.wav')
        sound_data = sound_data / (2. ** 15)
        fft_result = fft(sound_data)
        fft_length = int(len(fft_result) / 2)
        fft_result = abs(fft_result[0:fft_length - 1])
        fft_result = fft_result / max(fft_result)
        spectral_sum = numpy.sum(fft_result)
        self.send_message = str(spectral_sum)

    def plot_fft(self, fft):
        print(fft)
        Fs = 44100                      # sampling rate
        n = len(fft)                    # length of the signal
        k = numpy.arange(n)
        T = n / Fs
        frq = k / T                     # two sides frequency range
        # frq = frq[range(int(n / 2))]  # one side frequency range
        fig, ax = plt.subplots()
        ax.plot(frq, fft)
        plt.show()


class ServerClientConnection:
    def __init__(self, connection, address):
        self.connection = connection
        self.address = address

