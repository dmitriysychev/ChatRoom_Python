import socket
import sys


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 10000)
print (sys.stderr, 'staring up on %s port %s' % server_address)
sock.bind(server_address)

sock.listen(1)

while True:
    print (sys.stderr, 'waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print  (sys.stderr, 'connection from', client_address)

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(16384).decode()
            print (sys.stderr, 'received "%s"' % data)
            if data:
                print (sys.stderr, 'sending data back to the client')
                connection.sendall(data.encode())
            else:
                print (sys.stderr, 'no more data from', client_address)
                break
            
    finally:
        # Clean up the connection
        connection.close()