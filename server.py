import socket
import threading

hostname = input('Enter the hostname: ')
print('Hostname: ', hostname)
port = int(input('Enter the port number: '))
print('Port: ', port)

# Dictionary of all connected clients
clientsockets = {}

# Starting the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((hostname, port))
s.listen(5)

def accept_clients():
    while True:
        # Continuously checks for new client and accepts
        clientsocket, address = s.accept()
        print(f'{address} has joined the server.')

        data = clientsocket.recv(1024)
        clientname = data.decode('utf-8')

        # Message sent on joining
        clientsocket.send(bytes(f'Welcome to the chat {clientname}! If you want to leave, then enter "Leave".', 'utf-8'))
        # New thread for client
        threading.Thread(target = adding_to_chat, args = (clientsocket, clientname)).start()

def adding_to_chat(clientsocket, clientname):
    msg_send(' has joined the chat.', clientname)
    clientsockets[clientsocket] = clientname
    receiver = threading.Thread(
        target = msg_receive, args = (clientsocket, clientname), daemon = True
        ).start()

def msg_receive(clientsocket, clientname):
    while True:
        msg = clientsocket.recv(1024)
        decodedMsg = msg.decode('utf-8')

        if decodedMsg.lower() == 'leave':
            # Closes connection
            clientsocket.close()
            # Removes client from dictionary of connected clients
            del clientsockets[clientsocket]
            msg_send(' has left the chat.', clientname)
            break
        else:
            msg_send(decodedMsg, clientname)

def msg_send(message, name):
    if message == ' has left the chat.' or message == ' has joined the chat.':
        finalMsg = name + message
    else:
        finalMsg = name + ': ' + message
    
    # Sends message to all clients
    for client in clientsockets:
        client.send(bytes(finalMsg, 'utf-8'))


accept = threading.Thread(target = accept_clients)
accept.start()
accept.join()
s.close()
