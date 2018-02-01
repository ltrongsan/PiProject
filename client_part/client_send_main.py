import socket
import time
from client_part import client
import RecordAudio


host = socket.gethostname()
port = 8888

client1 = client.MyClient(host, port, 'MICROPHONE')
print('Connection Established')

while 1:
    client1.receive_message = client1.socket.recv(1024)
    if client1.receive_message.decode() == 'RECORD':
        # Start recording
        RecordAudio.record_audio()
        time.sleep(3)

        # Send FFT sum
        client1.sum_fourier_transform()
        client1.socket.send(client1.send_message.encode())
        print("FFT Sum was sent successfully")