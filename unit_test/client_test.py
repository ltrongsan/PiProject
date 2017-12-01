import socket
from client_part import client
import RecordAudio
import time

# Symbolic name, meaning all available interfaces
host = socket.gethostname()

# Arbitrary non-privileged
port = 8888

buffer_size = 1024

client1 = client.MyClient(host, port)

RecordAudio.record_audio()
time.sleep(2)

file = open('output.wav', 'rb')
client1.send_file(file, buffer_size)