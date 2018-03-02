import socket
import sys
import numpy
import time
import pygame
import pickle
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

        self.fft = None
        self.spectral_sum = None

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

    def send_record_file(self, file, buffer_size, command):
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

    def send_fft(self):
        rate, sound_data = wavfile.read('output.wav')
        self.fourier_transform(sound_data)
        serialized = pickle.dumps(self.fft)
        n = 0
        while n < len(serialized):
            if n < len(serialized) - 1023:
                print('Sending...')
                self.send_message = serialized[n:n+1023]
                self.socket.send(self.send_message)
                n = n + 1024
            else:
                print('Sending...')
                self.send_message = serialized[n:len(serialized)]
                self.socket.send(self.send_message)
                n = len(serialized)
        self.send_message = None

    def receive_fft(self):
        pass

    def fourier_transform(self, input_data):
        input_data = input_data / (2. ** 15)  # Convert sound data with 16 Bit
        self.fft = fft(input_data)
        fft_length = int(len(self.fft) / 2)  # Take only half of the FFT
        self.fft = abs(self.fft[0:fft_length - 1])  # Get the absolute value

    def sum_fourier_transform(self):
        rate, sound_data = wavfile.read('output.wav')
        sound_data = sound_data / (2. ** 15)            # Convert sound data with 16 Bit
        fft_result = fft(sound_data)
        fft_length = int(len(fft_result) / 2)           # Take only half of the FFT
        fft_result = abs(fft_result[0:fft_length - 1])  # Get the absolute value
        fft_result = fft_result / max(fft_result)       # Normalize the result
        self.fft = fft_result
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

        print("Done")

    def play_true_song(self):
        print("Play True Song")
        pygame.mixer.music.load("Cat.mp3")
        pygame.mixer.music.play(2)

    def play_false_song(self):
        print("Play False Song")
        pygame.mixer.music.load("Laugh.mp3")
        pygame.mixer.music.play(2)

    def stop_song(self):
        print("Stop playing Song")
        pygame.mixer.music.stop()