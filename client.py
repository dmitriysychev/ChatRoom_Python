import socket, random
import sys
import time 
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = input("Enter server IP or nothing to default: ")
HOST = (HOST if HOST != '' else 'localhost')

print('HOST : ' + HOST)

server_address = ('localhost', 3000)
print ('connecting to %s port %s\n' % server_address)

sock.connect(server_address)
sock.send(bytes("Test" + str(random.randint(0,10)), 'UTF-8'))

try:
    
    # Send data
    print(sock.recv(16384).decode()) # receives name request
    name = input()
    sock.sendall(bytes(name, encoding='UTF-8')) # we send name
    print(sock.recv(16384).decode()) # We receive response
    more = True
    while (more):
        #print("\nType 'closecon' to close connection\n\n")
        message = input("What message do you want to send: ")
        print ('sending "%s"' % message, end="")
        sock.sendall(bytes(message, encoding='UTF-8'))
        if (message == "logout"):
            more = False
            break
        data = sock.recv(16384).decode()
        if (message != 'history'):
            print ('\nreceived from server "%s"' % data)
        else:
            print('\n\nHistory of messages:\n%s' % data)
        check = input("Do you want to send more? y/n -->")
        more = True if check == "y" else False
finally:
    message = "logout"
    sock.sendall(message.encode())
    print ('closing socket')
    sock.close()
