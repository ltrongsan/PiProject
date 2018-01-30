import socket
from client_part import client


host = socket.gethostname()
port = 8888

client2 = client.MyClient(host, port, 'LOUDSPEAKER')
print('Connection Established')

while 1:
    # Receive and print out the sum of FFT spectral
    client2.receive()
    spectral_sum = float(client2.receive_message.decode())
    print(spectral_sum)


