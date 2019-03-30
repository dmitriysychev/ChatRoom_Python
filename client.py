import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 10000)
print ('connecting to "%s" port "%s"', server_address)

sock.connect(server_address)

try:
    
    # Send data
    more = True
    while (more):
        message = input("What message do you want to send (Type 'closecon' to close connection): ")
        
        print ('sending "%s"' % message)
        sock.sendall(bytes(message, encoding='UTF-8'))
        if (message == "closecon"):
            more = False
            break
        data = sock.recv(16384).decode()
        print ('received "%s"' % data)
        check = input("Do you want to send more? y/n -->")
        more = True if check == "y" else False
finally:
    message = "closecon"
    sock.sendall(message.encode())
    print ('closing socket')
    sock.close()