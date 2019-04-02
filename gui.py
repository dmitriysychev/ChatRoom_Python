from tkinter import *
import socket
import sys
import time 

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#initializing part
root = Tk()
root.geometry('800x400+200+100')

#connection block BEGIN
connectTo = LabelFrame(text = "Connect to")
paramFrame = Frame(connectTo)

connLabels = Frame(paramFrame)
labelHost = Label(connLabels, text = "Host", width = 25)
labelPort = Label(connLabels, text = "Port", width = 25)
labelUser = Label(connLabels, text = "Name", width = 25)

connEntry = Frame(paramFrame)
hostEntry = Entry(connEntry, width = 25)
portEntry = Entry(connEntry, width = 25)
userNameEntry = Entry(connEntry, width = 25)

connectButton = Button(connectTo, text = "Connect", width = 10, height = 1)
#connection block END

#body block BEGIN
bodyFrame = Frame()

onlineFrame = Frame(bodyFrame)
onlineLabel = Label(onlineFrame, text = "Online users")
onlineUsersList = Listbox(onlineFrame, height = 13)
passLabel = Label(onlineFrame, height = 4)

chatFrame = Frame(bodyFrame)
chatText = Text(chatFrame, height = 15)
messageFrame = Frame(chatFrame)
messageField = Text(messageFrame, width = 70, height = 3)
sendButton = Button(messageFrame, text = "Send", height = 3)

#body block END
#logic part
#functions defs
def connect(event):
    HOST = hostEntry.get()
    PORT = portEntry.get()
    userName = userNameEntry.get()
    #TODO preconditions
    server_address = (str(HOST), int(PORT))
    sock.connect(server_address)
    print(sock.recv(16384).decode())
    time.sleep(1)
    sock.sendall(bytes(userName, encoding='UTF-8'))
    print("Connection established")

connectButton.bind('<Button-1>', connect)


'''
e = Entry(root, width=20)
b = Button(root, text="Преобразовать")
l = Label(root, bg='black', fg='white', width=20)

def strToSortlist(event):
    s = e.get()
    s = s.split()
    s.sort()
    l['text'] = ' '.join(s)
 
b.bind('<Button-1>', strToSortlist)
 
e.pack()
b.pack()
l.pack()
'''

#rendering part
connectTo.pack(ipadx = 5, ipady = 5)

paramFrame.pack(side = LEFT)
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
passLabel.pack()
chatFrame.pack(side = RIGHT, ipady = 5)
chatText.pack(side = TOP)
messageFrame.pack(side = BOTTOM)
messageField.pack(side = LEFT, padx = 10)
sendButton.pack(side = RIGHT)

root.title("Messenger")
root.mainloop()