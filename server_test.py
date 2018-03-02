import socket
import time
import threading
from server_part import server
from server_part import threads


host = socket.gethostname()
port = 8888

server1 = server.MyServer(host, port)
connection, address = server1.socket.accept()
print('Connection established')
server1.receive_fft(connection)