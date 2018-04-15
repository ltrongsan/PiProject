from client_part import client
import socket
import time


isNotConnection = True
host = socket.gethostname()
port = 8888
while isNotConnection:
    try:
        camera_client = client.MyClient(host, port, 'CAMERA')
        print('Connection Established')
        isNotConnection = False
        while 1:
            camera_client.capture_video()
    except:
        isNotConnection = True
        print('CANNOT CONNECT TO SERVER')
        time.sleep(5)



