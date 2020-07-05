import socket
from tkinter import *
import threading

def msg_receive():
    while True:
        try:
            msg = s.recv(1024)
            decodedMsg = msg.decode('utf-8')
            myChat.insert(END, decodedMsg)
            myChat.pack(side = LEFT, fill = BOTH)
            myChat.yview(END)
        except:
            pass

def msg_send(event=None):
    message = myString.get()
    s.send(bytes(message, 'utf-8'))
    chatMsg.delete(0, 'end')
    chatMsg.pack()
    if message.lower() == 'leave':
        print('Closing connection...')
        s.close()
        root.destroy()
        print('Connection closed! Goodbye!')

hostname = input('Enter the hostname: ')
port = int(input('Enter the port number: '))
name = input('What is your name? ')

print('Connecting you to the server...')
justConnected = True

# Creating the client socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Attempt to connect to server
try:
    s.connect((hostname, port))
    print('Connection established!')
    print('Entering chat window...')
    s.send(bytes(name, 'utf-8'))

    # Creating the chat window
    root = Tk()

    myString = StringVar(root)

    frame = Frame(root)
    frame.pack()
    leftframe = Frame(root)
    leftframe.pack()
    bottomframe = Frame(root)
    bottomframe.pack()

    root.title('ChitChat')

    scrollbar = Scrollbar(leftframe)
    scrollbar.pack(side = RIGHT, fill = Y )

    myChat = Listbox(leftframe, width = 50, yscrollcommand = scrollbar.set)
    myChat.see(END)
    myChat.pack(side = LEFT, fill = BOTH)

    if justConnected == True:
        msg = s.recv(1024)
        decodedMsg = msg.decode('utf-8')
        myChat.insert(END, decodedMsg)
        myChat.pack(side = LEFT, fill = BOTH)
        justConnected = False

    instruction = Label(bottomframe, text='Enter your message below.')
    instruction.pack()

    chatMsg = Entry(bottomframe, textvariable = myString)
    chatMsg.bind('<Return>', msg_send)
    chatMsg.pack()
    chatMsg.focus_set()

    send = Button(bottomframe, text='Send', command = msg_send)
    send.pack()

    read_thread = threading.Thread(target = msg_receive, daemon = True)
    read_thread.start()

    mainloop()

except socket.gaierror:
    print('Connection failed. No server found.')
