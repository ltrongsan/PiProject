import socket
import sys
import numpy
import time
import pygame
import pickle
import cv2
from scipy.io import wavfile
from numpy.fft import fft


class MyClient:
    """

    """
    def __init__(self, host, port, type):
        self.client_IP = socket.gethostname()
        self.send_message = None
        self.receive_message = None
        self.file_size = 0
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)     # create an INET, STREAMing socket

        self.command = None
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
        """

        :param file:
        :param buffer_size:
        :param command:
        :return:
        """
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

    def send_fft(self):
        """

        :return:
        """
        buffer_size = 4096
        packet_number = 0
        sent_size = 0

        self.receive_command()
        rate, sound_data = wavfile.read('output.wav')
        self.fourier_transform(sound_data)
        serialized = pickle.dumps(self.fft)
        obj_size = len(serialized)
        self.send_message = str(obj_size)

        if self.command == "GET FFT":
            self.socket.send(self.send_message.encode())
            self.send_message = None
            while obj_size > 0:
                if obj_size > buffer_size:
                    print('Sending...')
                    self.send_message = serialized[buffer_size*packet_number:
                                                   buffer_size*packet_number + buffer_size]
                    self.socket.send(self.send_message)
                    self.send_message = None
                    obj_size = obj_size - buffer_size
                    packet_number += 1
                    sent_size += len(serialized[buffer_size*packet_number:
                                                buffer_size*packet_number + buffer_size])
                else:
                    self.send_message = serialized[buffer_size*packet_number: len(serialized)]
                    self.socket.send(self.send_message)
                    sent_size += len(serialized[buffer_size*packet_number: len(serialized)])
                    break
        self.send_message = None

    def receive_command(self):
        """

        :return:
        """
        self.command = self.socket.recv(2048)
        self.command = self.command.decode()

    def fourier_transform(self, input_data):
        """

        :param input_data:
        :return:
        """
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

    def receive_song(self, isTrueSong):
        """

        :param isTrueSong:
        :return:
        """
        buffer_size = 4096
        if isTrueSong:
            print('Receive TRUE Sound')
            file_name = "True Sound.mp3"
        else:
            print('Receive FALSE Sound')
            file_name = "False Sound.mp3"

        file = open(file_name, "w+b")
        data = self.socket.recv(buffer_size)
        string = 'DONE'
        string = string.encode()
        print(string)
        while data != string:
            print('Receiving sound ...')
            file.write(data)
            print(str(list(data)))
            data = self.socket.recv(buffer_size)

        file.close()
        print("Done")

    def play_true_song(self, loop):
        """

        :param loop:
        :return:
        """
        try:
            print("Play True Sound")
            pygame.mixer.music.load("True Sound.mp3")
            pygame.mixer.music.play(loop)
        except:
            print('Cannot play. Please configure the sound first')

    def play_false_song(self, loop):
        """

        :param loop:
        :return:
        """
        try:
            print("Play False Sound")
            pygame.mixer.music.load("False Sound.mp3")
            pygame.mixer.music.play(loop)
        except:
            print('Cannot play. Please configure the sound first')

    def stop_song(self):
        """

        :return:
        """
        print("Stop playing Sound")
        pygame.mixer.music.stop()

    def show_webcam(self, mirror=False):
        cam = cv2.VideoCapture(0)
        while True:
            ret_val, img = cam.read()
            if mirror:
                img = cv2.flip(img, 1)
            cv2.imshow('my webcam', img)
            if cv2.waitKey(1) == 27:
                break  # esc to quit
        cv2.destroyAllWindows()

    def send_image(self):
        pass

