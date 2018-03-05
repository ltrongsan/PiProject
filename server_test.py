import socket
import time
import threading
from server_part import server
from server_part import threads


host = socket.gethostname()
# host = (([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [
#             [(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in
#              [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0]
port = 8888

server1 = server.MyServer(host, port)
connection, address = server1.socket.accept()
print('Connection established')
server1.receive_fft(connection)