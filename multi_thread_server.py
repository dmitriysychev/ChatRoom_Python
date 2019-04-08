import socket, threading, time
from datetime import datetime
class ClientThread(threading.Thread):
       
        def __init__(self,clientAddress,clientsocket,messages,clients, users, db):
                threading.Thread.__init__(self)
                clients.append(clientAddress)
                db.insertClient(clientAddress)
                self.csocket = clientsocket
                self.clientAddress = clientAddress
                print ("New connection added: ", self.clientAddress)
        def run(self):
                print ("Connection from : ", self.clientAddress)
                name = ''
                nameReceived = False
                while (not nameReceived):
                    name = self.csocket.recv(1024).decode()
                    self.csocket.send(bytes("Hello, nice to meet you, %s" % name, 'utf-8'))
                    users.append(name)
                    nameReceived = True
                db.clients[self.clientAddress] = name
                msg = ''
                while True:
                    data = self.csocket.recv(2048)
                    timeNow = datetime.now()
                    current_time = timeNow.strftime("%H:%M:%S")
                    msg = data.decode()
                    
                    if msg=='bye':
                        #TODO fix clients update
                        users.remove(name)
                        db.remove(name)
                        break
                    elif msg.find('/history') > -1:
                        toUser = msg.split(' ')[1]
                        fromUser = name
                        hist = db.showHistory(toUser, fromUser)
                        toSend = ' '.join(hist)
                        if len(toSend) < 2:
                            toSend = "No messages |"
                        self.csocket.send(bytes(toSend,'UTF-8'))
                    elif msg.find("/online") > -1 :
                        self.csocket.send(bytes(' '.join(str(elem) for elem in users), 'UTF-8'))
                    elif msg.find("/sendto") > -1:
                        fromName = db.getClientName(self.clientAddress)
                        toWhom = msg.split(' ')[1]
                        print(msg.split(' '))
                        #print(' '.join(str(el) for el in msg.split(' ')[2:(len(msg) - len(current_time))]))
                        db.append(fromName, toWhom, ' '.join(str(el) for el in msg.split(' ')[2:(len(msg) - len(current_time))]), current_time)
                    else:
                        messages.append([name, msg, current_time])
                        self.csocket.send(bytes("ERRORRRRR",'UTF-8'))
                print ("Client ", db.getClientName(self.clientAddress) , " disconnected...")

class DataBase(object):
    #FOR COMMIT
            #Main dictionary to store addresses and names
            clients = {} # {addr: name}
            history = [] # [[namefrom, nameto, msg, time], [-||-]]
            data = []
            def __init__(self):
                print("Database created")

            '''
            Function to insert client in the database
            '''
            def insertClient (self, addr):
                oldSize = len(self.clients)
                if addr not in self.clients:
                    self.clients[addr] = 0
                return oldSize != len(self.clients)

            def changeName(self, addr, name):
                if addr in self.clients:
                    self.clients[addr] = name
            '''
            Function to get a client address based on its name
            @param name - client name to find its address
            '''
            def getClientAddr(self, name):
                for client in self.clients:
                    if self.clients[client] == name:
                        return client

            '''
            Function to get a client name based on its address
            @param addr - client address to find its name
            '''
            def getClientName(self, addr):
                for client in self.clients:
                    if client == addr:
                        return self.clients[client]
            '''
            Function to return the number of clients
            '''
            def size(self):    
                return len(self.clients)

            '''
            Function to add history of messages in the format 
            [fromClient, toClient, message, timeSent]
            @param fromClient - name of the client that sent msg
            @param toClient - name of the client msg was sent
            @msg - message that was sent
            @time - time the message was sent to client
            '''
            def append(self, fromClient_name, toClient_name, msg, time):
                self.history.append([fromClient_name, toClient_name, msg, time])
                
            '''
            Function to print history 
            '''
            def showHistory(self, fromClient_name, toClient_name):
                historyArr = []
                retVal = []
                for unit in self.history:
                        if unit[0] == fromClient_name and unit[1] == toClient_name:
                                historyArr.append(unit)
                        del unit
                for hist in historyArr:
                        rec = str(hist[0]) + "~" + str(hist[1]) + "~" + str(hist[2]) + "~" + str(hist[3]) + "|"
                        retVal.append(rec)
                        del hist
                return retVal         
            '''
            Function to remove client from a database
            @param name - name of the client to be removed
            '''
            def remove(self, name):
                oldsize = self.size()
                for client in self.clients:
                    if self.clients[client] == name:
                        del client
                return oldsize != self.size()


       
                

LOCALHOST = "localhost"
PORT = 3000
messages = []
clients = []
users = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LOCALHOST, PORT))

print("Server started")
print("Waiting for client request..")

while True:
    server.listen(1)
    clientsock, clientAddress = server.accept()
    db = DataBase()
    newthread = ClientThread(clientAddress, clientsock, messages, clients, users, db)
    newthread.start()
