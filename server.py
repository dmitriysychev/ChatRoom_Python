import socket
import sys


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 10000)
print ('staring up on %s port %s' % server_address)
sock.bind(server_address)

sock.listen(2)
client = True
while (client):
    print ('waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print  ('connection from', client_address)
        connection.send(bytes("Hello " + str(client_address), encoding='UTF-8'))
        # Receive the data in small chunks and retransmit it
        connected = True
        while (connected):
            data = connection.recv(16384).decode()
            print ('received "%s"' % data)
            if (data == "closecon"):
                connected = False
                client = False
                break
            if data:
                print ('sending data back to the client')
                connection.sendall(bytes(data, encoding='UTF-8'))
            else:
                print ('no more data from', client_address)
                break
            
    finally:
        # Clean up the connection
        connection.close()
        #sock.close()
print("Closing socket")
sock.close()