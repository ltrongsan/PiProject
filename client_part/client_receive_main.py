import socket
from client_part import client
import pygame


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
        client2.play_true_song()
    else:
        client2.play_false_song()

