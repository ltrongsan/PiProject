import socket
from client_part import client
import pygame


def start_true_song():
    print("Start True Song")
    pygame.mixer.music.load("True.mp3")
    pygame.mixer.music.play(-1)


def start_false_song():
    print("Would False Song")
    pygame.mixer.music.load("False.mp3")
    pygame.mixer.music.play(-1)


def stop_song():
    print("Would Stop Song")
    pygame.mixer.music.stop()


host = socket.gethostname()
port = 8888

client2 = client.MyClient(host, port, 'LOUDSPEAKER')
print('Connection Established')

pygame.mixer.init()

while 1:
    # Receive and print out the sum of FFT spectral
    client2.receive_message = client2.socket.recv(1024)
    spectral_sum = float(client2.receive_message.decode())
    print(spectral_sum)
    if spectral_sum > 650:
        start_true_song()
    else:
        start_false_song()

