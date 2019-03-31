import socket
import sys
import time 
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('212.116.121.138', 3000)
print ('connecting to %s port %s\n' % server_address)

sock.connect(server_address)

try:
    
    # Send data
    print(sock.recv(16384).decode())
    time.sleep(1)
    more = True
    while (more):
        print("\nType 'closecon' to close connection\n\n")
        message = input("What message do you want to send: ")
        print ('sending "%s"' % message, end="")
        # for i in range(4):
        #     sys.stdout.write('.')
        #     sys.stdout.flush()
        #     time.sleep(0.5)
            
        sock.sendall(bytes(message, encoding='UTF-8'))
        if (message == "closecon"):
            more = False
            break
        data = sock.recv(16384).decode()
        print ('\nreceived from server "%s"' % data)
        check = input("Do you want to send more? y/n -->")
        more = True if check == "y" else False
finally:
    message = "closecon"
    sock.sendall(message.encode())
    print ('closing socket')
    sock.close()