from tkinter import *
import socket, random
import sys
import time 

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
isEstablished = False
#pirnt
#initializing part
root = Tk()
root.geometry('800x400+200+100')
root.resizable(False, False)

#connection block BEGIN
connectTo = LabelFrame(text = "Connect to")
paramFrame = Frame(connectTo)

connLabels = Frame(paramFrame)
labelHost = Label(connLabels, text = "Host", width = 25)
labelPort = Label(connLabels, text = "Port", width = 25)
labelUser = Label(connLabels, text = "Name", width = 25)

connEntry = Frame(paramFrame)
hostEntry = Entry(connEntry, width = 25)
hostEntry.delete(0,END)
hostEntry.insert(0, "localhost")
portEntry = Entry(connEntry, width = 25)
portEntry.delete(0,END)
portEntry.insert(0, "3000")
userNameEntry = Entry(connEntry, width = 25)
userNameEntry.delete(0,END)
userNameEntry.insert(0, "Test" + str(random.randint(10,99)))

statusLabel = Label(connectTo, width = 5, height = 5, bg = "red")
connectButton = Button(connectTo, text = "Connect", width = 10, height = 1)
#connection block END

#body block BEGIN
bodyFrame = Frame()

onlineFrame = Frame(bodyFrame)
onlineLabel = Label(onlineFrame, text = "Online users")
onlineUsersList = Listbox(onlineFrame, height = 13)
passLabel = Label(onlineFrame, height = 4)

chatFrame = LabelFrame(bodyFrame, text = "Chat")
chatText = Text(chatFrame, height = 15)
messageFrame = Frame(chatFrame)
messageField = Text(messageFrame, width = 70, height = 3)
sendButton = Button(messageFrame, text = "Send", height = 3)

#body block END
#logic part
#functions defs
def connect(event):
    global isEstablished
    HOST = hostEntry.get()
    PORT = portEntry.get()
    userName = userNameEntry.get()
    #TODO preconditions
    server_address = (str(HOST), int(PORT))
    sock.connect(server_address)
    sock.send(bytes(userName, encoding='UTF-8'))
    if (len(sock.recv(16384).decode()) > 0):
        #if connection established
        statusLabel.configure(bg = "green")
        isEstablished = True
        onlineUsersList.after_idle(updateUsers)


connectButton.bind('<Button-1>', connect)   

def updateUsers():
    onlineUsersList.after(1000, updateUsers)
    if isEstablished:
        sock.send(bytes("/online", encoding='UTF-8'))
        onlineUsers = sock.recv(16384).decode().split(' ')
        oldList = onlineUsersList.get(0, END)
        i = 0
        
        for elem in oldList:
            #if old items not in new - delete them
            if elem not in onlineUsers:
                onlineUsersList.delete(i,i)
            else:
                onlineUsers.remove(elem)
            i += 1
        for elem in onlineUsers:
            onlineUsersList.insert(END, elem)

def openChat(evt):
    w = evt.widget
    index = int(w.curselection()[0])
    value = w.get(index)
    chatFrame.configure(text = "Chat with " + value)
    chatText.after(100, getHistory)

def getHistory():
    chatText.after(500, getHistory)
    toUser= chatFrame['text'].split(' ')[2]
    sock.send(bytes("/history " + toUser,'UTF-8'))
    history = sock.recv(16384).decode().split('|')
    chatText.delete(1.0, END)
    #print("This is history: %s" % history)
    for rec in history:
        rec = rec.split('~')
        #print("THis is rec %s " % rec)
        #TODO fix parse
        try:
            toPrint = str(rec[3]) + '>>\t' + ''.join((str(msg) for msg in rec[2]))
            chatText.insert(END, toPrint+'\n')
        except:
            continue
        del rec
    '''
    userTo = onlineUsersList.get(int(onlineUsersList.curselection()[0]))
    sock.send(bytes("/history "+userTo, 'UTF-8'))
    history = sock.recv(16384).decode()
    #TODO insert history
    history = history.split('|')
    chatText.delete(1.0, END)
    for rec in history:
        chatText.insert(END, rec) 
    print(history)
    '''
#this is rec ['Test94', 'Test37', "['HELLO', 'WASUP\\n']", '17:59:38 Test94', 'Test37', "['OLA', 'AMIGO\\n']", '17:59:56']
def window_deleted():
    sock.send(bytes("bye", 'UTF-8'))
    root.quit()

def sendMessage(self):
    userTo = onlineUsersList.get(int(onlineUsersList.curselection()[0]))
    messageText = messageField.get(1.0, END)
    sock.send(bytes("/sendto " + userTo + " " + messageText, 'UTF-8'))
    messageField.delete(1.0,END)

sendButton.bind('<Button-1>', sendMessage)
#rendering part
connectTo.pack(ipadx = 5, ipady = 5)

paramFrame.pack(side = LEFT)
statusLabel.pack(side = LEFT)
connectButton.pack(side = RIGHT)

connLabels.pack()
connEntry.pack()
labelHost.pack(side = LEFT)
labelPort.pack(side = LEFT)
labelUser.pack(side = LEFT)
hostEntry.pack(side = LEFT)
portEntry.pack(side = LEFT)
userNameEntry.pack(side = LEFT)

bodyFrame.pack()
onlineFrame.pack(side = LEFT)
onlineLabel.pack()
onlineUsersList.pack()
onlineUsersList.bind('<<ListboxSelect>>', openChat)
passLabel.pack()
chatFrame.pack(side = RIGHT, ipady = 5)
chatText.pack(side = TOP)
messageFrame.pack(side = BOTTOM)
messageField.pack(side = LEFT, padx = 10)
sendButton.pack(side = RIGHT)

root.title("Messenger")
root.protocol('WM_DELETE_WINDOW', window_deleted)
root.mainloop()
