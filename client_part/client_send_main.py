import socket
import time
from client_part import client
import RecordAudio


host = socket.gethostname()
port = 8888
buffer_size = 1024

client1 = client.MyClient(host, port)
print('Connection Established')

while 1:
    client1.receive_message = client1.socket.recv(1024)
    if client1.receive_message.decode() == 'RECORD':
        # Start recording
        RecordAudio.record_audio()
        time.sleep(3)

        # Send file
        file = open('output.wav', 'rb')
        client1.send_file(file, buffer_size, 'SEND')
        file.close()

    client1 = client.MyClient(host, port)

