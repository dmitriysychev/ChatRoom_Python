import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 10000)
print (sys.stderr, 'connecting to %s port %s', server_address)

sock.connect(server_address)

try:
    
    # Send data
    message = 'This is the message.  It will be repeated.'
    print (sys.stderr, 'sending "%s"' % message)
    sock.sendall(message.encode())

    # Look for the response
    amount_received = 0
    amount_expected = len(message)
    
    while amount_received < amount_expected:
        data = sock.recv(16384).decode()
        amount_received += len(data)
        print (sys.stderr, 'received "%s"' % data)

finally:
    print (sys.stderr, 'closing socket')
    sock.close()