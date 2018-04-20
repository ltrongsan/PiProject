import socket
import time
import pygame
from client_part import client



isNotConnection = True
host = socket.gethostname()
port = 8888
pygame.mixer.init()
while isNotConnection:
    try:
        loudspeaker_client = client.MyClient(host, port, 'LOUDSPEAKER')
        print('Connection Established')
        isNotConnection = False
        while 1:
            # Receive and print out the sum of FFT spectral
            loudspeaker_client.receive_message = loudspeaker_client.socket.recv(1024)
            message = loudspeaker_client.receive_message.decode()
            print(message)
            if message == 'TRUE':
                loudspeaker_client.play_true_song(2)
            elif message == 'FALSE':
                loudspeaker_client.play_false_song(2)
            elif message == 'STOP':
                loudspeaker_client.stop_song()
            elif message == 'PLAY TRUE':
                loudspeaker_client.play_true_song(-1)
            elif message == 'PLAY FALSE':
                loudspeaker_client.play_false_song(-1)
            elif message == 'CONFIGURE TRUE':
                loudspeaker_client.receive_song(True)
            elif message == 'CONFIGURE FALSE':
                loudspeaker_client.receive_song(False)
            else:
                continue
    except:
        isNotConnection = True
        print('CANNOT CONNECT TO SERVER')
        time.sleep(5)



