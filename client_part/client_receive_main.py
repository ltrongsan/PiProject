import socket
import time
from client_part import client
import pygame


isNotConnection = True
host = socket.gethostname()
port = 8888
pygame.mixer.init()
while isNotConnection:
    try:
        client2 = client.MyClient(host, port, 'LOUDSPEAKER')
        print('Connection Established')
        isNotConnection = False
        while 1:
            # Receive and print out the sum of FFT spectral
            client2.receive_message = client2.socket.recv(1024)
            message = client2.receive_message.decode()
            print(message)
            if message == 'TRUE':
                client2.play_true_song(2)
            elif message == 'FALSE':
                client2.play_false_song(2)
            elif message == 'STOP':
                client2.stop_song()
            elif message == 'PLAY TRUE':
                client2.play_true_song(-1)
            elif message == 'PLAY FALSE':
                client2.play_false_song(-1)
            elif message == 'CONFIGURE TRUE':
                client2.receive_song(True)
            elif message == 'CONFIGURE FALSE':
                client2.receive_song(False)
            else:
                continue
    except:
        isNotConnection = True
        print('CANNOT CONNECT TO SERVER')
        time.sleep(5)



