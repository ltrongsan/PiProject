import socket
import time
from client_part import client
import RecordAudio


host = socket.gethostname()
port = 8888

client1 = client.MyClient(host, port, 'MICROPHONE')
print('Connection Established')

client1.send_fft()