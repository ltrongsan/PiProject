import socket
import time
import numpy
from scipy.io import wavfile
from numpy.fft import fft
import RPi.GPIO as GPIO


class MyClient:
    def __init__(self, host, port):

        self.send_message = None
        self.receive_message = None
        self.file_size = 0
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.led_pin = 7    # GPIO output pin number

        # Connect the socket to the port where the server is listening
        server_address = (host, port)
        print('connecting to %s port %s' % server_address)
        self.socket.connect(server_address)

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
        # print(self.socket.recv(1024))
        self.socket.close()

    def receive(self):
        command = 'RECEIVE'
        self.send_message = command.encode()    # Send command message 'RECEIVE'
        self.socket.send(self.send_message)
        self.receive_message = self.socket.recv(1024)

    def setup_pi(self):
        GPIO.setmode(GPIO.BOARD)                # Numbers GPIOs by physical location
        GPIO.setup(self.led_pin, GPIO.OUT)      # Set LedPin's mode is output
        GPIO.output(self.led_pin, GPIO.HIGH)    # Set LedPin high(+3.3V) to turn on led

    def blink(self):
        while True:
            GPIO.output(self.led_pin, GPIO.HIGH)  # LED on
            time.sleep(1)
            GPIO.output(self.led_pin, GPIO.LOW)  # LED off
            time.sleep(1)

    def destroy(self):
        GPIO.output(self.led_pin, GPIO.LOW)     # LED off
        GPIO.cleanup()                          # Release resource

    def sum_fourier_transform(self):
        rate, sound_data = wavfile.read('output.wav')
        sound_data = sound_data / (2. ** 15)            # Convert sound data with 16 Bit
        fft_result = fft(sound_data)
        fft_length = int(len(fft_result) / 2)           # Take only half of the FFT
        fft_result = abs(fft_result[0:fft_length - 1])  # Get the absolute value
        fft_result = fft_result / max(fft_result)       # Normalize the result
        spectral_sum = numpy.sum(fft_result)
        self.send_message = str(spectral_sum)