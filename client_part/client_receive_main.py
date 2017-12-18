import socket
from client_part import client


host = socket.gethostname()
port = 8888

client1 = client.MyClient(host, port)
print('Connection Established')

# Receive and print out the sum of FFT spectral
client1.receive()
spectral_sum = float(client1.receive_message.decode())
print(spectral_sum)
