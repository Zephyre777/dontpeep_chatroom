import socket
from threading import Thread
from utils import Server, Client_instance

HEADER_LENGTH = 16
host = "127.0.0.1"
port = 500  # initiate port no above 1024
client_list = []

def send(socket, msg):
    msg = str(msg).encode('utf-8')
    msg_hdr = f"{len(msg):<{HEADER_LENGTH}}".encode('utf-8') #left-align with length [HEADER_LENGTH]

    #send the utf-8 encoded msg
    print("Send: " + str(msg, "utf-8"))
    socket.send(msg_hdr+msg)

def receive(socket):
    msg_hdr = socket.recv(HEADER_LENGTH) #read header
    msg_len = int(msg_hdr.decode('utf-8').strip()) #decode msg length
    msg_payload = socket.recv(msg_len) #read msg
    msg = msg_hdr + msg_payload
    print("Receive: " + str(msg))
    return msg_payload

def broadcast(msg, userName):
    print("broadcast")
    for client in client_list:
        if(client.name != userName):
            client.send(msg)

def receive_handler(socket, userName):
    while True:
        msg = receive(socket)
        broadcast(msg, userName)

def chat(socket, userName):
    print("autheticate")
    receive_thread = Thread(target = receive_handler, args = (socket, userName, )) # Receive msg from client program
    receive_thread.start()
    receive_thread.join()

def initialization(socket, server):
    print("Request for user name")
    userName = receive(socket)
    # client_list[userName] = socket
    # client_list.append(socket)
    # socket.name = userName
    print("Return p")
    send(socket, server.p)
    server.publicKeys.append(int(receive(socket)))
    return userName

def server_program():
    # get the hostname
    print(host)
    
    global server
    server = Server()
    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # queue up as many as 5 connect requests (the normal max) before refusing outside connections
    server_socket.listen(5)
    while True:
        client, cli_address = server_socket.accept()  # accept new connection
        print("Receive Connection Request from: " + str(cli_address))
        # receive data stream. it won't accept data packet greater than 1024 bytes
        client_socket = Client_instance
        client_socket.socket = client
        userName = initialization(client, server)
        client_socket.name = userName
        client_list.append(client_socket)
        Thread(target = chat, args = (client, userName, )).start()




if __name__ == '__main__':
    server_program()