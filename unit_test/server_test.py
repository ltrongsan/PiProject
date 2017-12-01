import socket
from server_part import server

host = socket.gethostname()
port = 8888

server1 = server.MyServer(host, port)

while 1:
    # now keep talking with the client
    # wait to accept a connection - blocking call
    conn, address = server1.socket.accept()
    print('Connected with ' + address[0] + ':' + str(address[1]))

    print("Receiving...")
    l = conn.recv(1024)
    file = open('test.wav', 'wb')
    while (l):
        print("Receiving...")
        file.write(l)
        l = conn.recv(1024)
    file.close()
    print("Done Receiving")
    conn.send('Thank you for connecting')
    conn.close()  # Close the connection


