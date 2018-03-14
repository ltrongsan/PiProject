import socket
import time
from client_part import client
import RecordAudio


isNotConnection = True
host = socket.gethostname()
port = 8888
while isNotConnection:
    try:
        client1 = client.MyClient(host, port, 'MICROPHONE')
        print('Connection Established')
        isNotConnection = False
        while 1:
            client1.receive_message = client1.socket.recv(1024)
            if client1.receive_message.decode() == 'RECORD':
                # Start recording
                RecordAudio.record_audio()
                time.sleep(3)

                # Send FFT sum
                client1.send_fft()
                print("FFT was sent successfully")
    except:
        print('CANNOT CONNECT TO SERVER')
        isNotConnection = True
        time.sleep(5)

