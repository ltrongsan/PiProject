import socket
import time
from client_part import client


host = socket.gethostname()
port = 8888
buffer_size = 1024

client1 = client.MyClient(host, port)
print('Connection Established')

# Receive and print out the sum of FFT spectral
client1.receive()
spectral_sum = float(client1.receive_message.decode())
print(spectral_sum)

# Blink the LED
# if spectral_sum < 900:
#     client1.setup_pi()
#     for i in range(0, 10):
#         client1.blink()
#     client1.destroy()
# else:
#     client1.setup_pi()
#     time.sleep(15)
#     client1.destroy()