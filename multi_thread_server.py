import socket, threading, time
from datetime import datetime
class ClientThread(threading.Thread):
       
        def __init__(self,clientAddress,clientsocket,messages,clients, users, db):
                threading.Thread.__init__(self)
                clients.append(clientAddress)
                db.insertClient(clientAddress)
                self.csocket = clientsocket
                print ("New connection added: ", clientAddress)
        def run(self):
                print ("Connection from : ", clientAddress)
                name = ''
                nameReceived = False
                while (not nameReceived):
                    #self.csocket.send(bytes("Hi, What is your name?",'utf-8'))
                    name = self.csocket.recv(1024).decode()
                    self.csocket.send(bytes("Hello, nice to meet you, %s" % name, 'utf-8'))
                    users.append(name)
                    db.changeName(clientAddress, name)
                    nameReceived = True
                msg = ''
                print("DB SIZE IS {size}".format(size = db.size())) # debug check
                while True:
                    data = self.csocket.recv(2048)
                    timeNow = datetime.now()
                    current_time = timeNow.strftime("%H:%M:%S")
                    msg = data.decode()
                    
                    if msg=='bye':
                        #TODO fix clients update
                        users.remove(name)
                        db.remove(name)
                        #clients.remove(clientAddress)
                        break
                    if msg=='history':
                        self.csocket.send(bytes('\n'.join([' | '.join(str(aaa) for aaa in message) for message in messages]),'UTF-8'))
                    elif msg.find("/from") > -1 :
                        userName = msg.split(' ')[1]
                        print("User {name} waiting messages from {userName}".format(name=name, userName = userName))
                        messageSent = False
                        startTime = timeNow.strftime("%H:%M:%S")
                        while(not messageSent):
                            newMessages = []
                            for elemHist in messages:
                                if(timeNow.strptime(elemHist[2], "%H:%M:%S") > timeNow.strptime(startTime, "%H:%M:%S") and elemHist[0] == userName):
                                    newMessages.append([elemHist[2], elemHist[1]])
                            if (len(newMessages) > 0):
                                self.csocket.send(bytes('\n'.join(['\t'.join(str(aaa) for aaa in message) for message in newMessages]),'UTF-8'))
                                messageSent = True
                            time.sleep(1)
                    elif msg.find("/online") > -1 :
                        self.csocket.send(bytes(' '.join(str(elem) for elem in users), 'UTF-8'))
                    elif msg.find("/sendto") > -1:
                        fromName = db.getClientName(clientAddress)
                        toWhom = msg.split(' ')[1]
                        db.append(fromName, toWhom, msg.split(' ')[2:], current_time)
                        print(db.showHistory(fromName, toWhom))
                    else:
                        messages.append([name, msg, current_time])
                        print ("from client", msg)
                        self.csocket.send(bytes(msg,'UTF-8'))
                print ("Client at ", clientAddress , " disconnected...")

class DataBase(object):
            #Main dictionary to store addresses and names
            clients = {} # {name: (addr, port)}
            # TODO choose the best choice for storing history
            history = [] # [[namefrom, nameto, msg, history], [-||-]]
            data = []
            def __init__(self):
                print("Database created")

            '''
            Function to insert client in the database
            '''
            def insertClient (self, addr):
                oldSize = len(self.clients)
                if addr not in clients:
                    self.clients[addr] = 0
                return oldSize != len(self.clients)

            def changeName(self, addr, name):
                if addr in clients:
                    self.clients[addr] = name
            '''
            Function to get a client address based on its name
            @param name - client name to find its address
            '''
            def getClientAddr(self, name):
                return self.clients[name]

            '''
            Function to get a client name based on its address
            @param addr - client address to find its name
            '''
            def getClientName(self, addr):
                for client in self.clients:
                    if self.clients[client] == addr:
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
                #oldsize = len(self.history)
                self.history.append([fromClient_name, toClient_name, msg, time])
                #return oldsize != len(self.history)
                
            '''
            Function to print history 
            '''
            def showHistory(self, fromClient_name, toClient_name):
                historyArr = []
                for unit in self.history:
                        if unit[0] == fromClient_name and unit[1] == toClient_name:
                                historyArr.append(unit)
                for hist in historyArr:
                        print("Sent from {fromC} to {toC}: \'{message}'\, sent at {timeSent}".format(fromC = fromClient_name, toC = toClient_name, message = hist[2], timeSent = hist[3]))
                        
            '''
            Function to remove client from a database
            @param name - name of the client to be removed
            '''
            def remove(self, name):
                oldsize = self.size()
                for client in clients:
                    if clients[client] == name:
                        del clients[client]
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
