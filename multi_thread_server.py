import socket, threading
class ClientThread(threading.Thread):
        def __init__(self,clientAddress,clientsocket,messages,clients):
                threading.Thread.__init__(self)
                clients.append(clientAddress)
                self.csocket = clientsocket
                print ("New connection added: ", clientAddress)
        def run(self):
                print ("Connection from : ", clientAddress)
                name = ''
                nameSend = False
                while (not nameSend):
                    self.csocket.send(bytes("Hi, What is your name?",'utf-8'))
                    name = self.csocket.recv(1024).decode()
                    self.csocket.send(bytes("Hello, nice to meet you, ",'utf-8'))
                    nameSend = True
                msg = ''
                while True:
                    data = self.csocket.recv(2048)
                    msg = data.decode()
                    if msg=='bye':
                        break
                    if msg=='history':
                        self.csocket.send(bytes('\n'.join([' | '.join(str(aaa) for aaa in message) for message in messages]),'UTF-8'))
                    else:
                        messages.append([name, msg])
                        print ("from client", msg)
                        self.csocket.send(bytes(msg,'UTF-8'))
                    print ("Client at ", clientAddress , " disconnected...")

LOCALHOST = "localhost"
PORT = 3000
messages = []
clients = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LOCALHOST, PORT))

print("Server started")
print("Waiting for client request..")

while True:
    server.listen(1)
    clientsock, clientAddress = server.accept()
    newthread = ClientThread(clientAddress, clientsock, messages, clients)
    newthread.start()





