import socket
import time
from client_part import client
import RecordAudio


isConnection = False
host = socket.gethostname()
port = 8888
while not isConnection:
    try:
        client1 = client.MyClient(host, port, 'MICROPHONE')
        print('Connection Established')
        isConnection = True
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
        isConnection = False
        print('CANNOT CONNECT TO SERVER')
        time.sleep(5)

