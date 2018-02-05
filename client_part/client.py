import socket
import sys
import numpy
import time
import threading
from scipy.io import wavfile
from numpy.fft import fft
import matplotlib.pyplot as plt


class MyClient:
    def __init__(self, host, port, type):
        self.client_IP = socket.gethostname()
        self.send_message = None
        self.receive_message = None
        self.file_size = 0
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)     # create an INET, STREAMing socket

        # Connect the socket to the port where the server is listening
        server_address = (host, port)
        print('connecting to %s port %s' % server_address)
        try:
            self.socket.connect(server_address)
            self.socket.send(type.encode())
            time.sleep(2)
        except socket.error as msg:
            print('Bind failed. Error Code : ' + str(msg))
            sys.exit()

    def send_file(self, file, buffer_size, command):
        # Send command message (ex. 'SEND')
        self.send_message = command.encode()
        self.socket.send(self.send_message)

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
        self.socket.shutdown(socket.SHUT_WR)
        self.socket.close()

    def sum_fourier_transform(self):
        rate, sound_data = wavfile.read('output.wav')
        sound_data = sound_data / (2. ** 15)            # Convert sound data with 16 Bit
        fft_result = fft(sound_data)
        fft_length = int(len(fft_result) / 2)           # Take only half of the FFT
        fft_result = abs(fft_result[0:fft_length - 1])  # Get the absolute value
        self.plot_fft(fft_result)
        # t1 = threading.Thread(target=lambda: self.plot_fft(fft))
        # t1.start()
        # t1.join()
        fft_result = fft_result / max(fft_result)       # Normalize the result
        spectral_sum = numpy.sum(fft_result)
        self.send_message = str(spectral_sum)

    def plot_fft(self, fft):
        print(fft)

        Fs = 44100                  # sampling rate
        n = len(fft)                # length of the signal
        k = numpy.arange(n)
        T = n / Fs
        frq = k / T                 # two sides frequency range
                                    # frq = frq[range(int(n / 2))]  # one side frequency range

        fig, ax = plt.subplots()
        ax.plot(frq, fft)
        plt.show()

    def receive_sound(self, isTrue):
        if isTrue:
            print('Receive TRUE Sound')
            file_name = "True.wav"
        else:
            print('Receive FALSE Sound')
            file_name = "False.wav"

        file = open(file_name, "w+b")
        while True:
            data = self.socket.recv(1024)
            if not data:
                break
            file.write(data)
            print(str(list(data)))

        print("Done.")