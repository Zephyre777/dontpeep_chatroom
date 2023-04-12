import socket
from threading import Thread

HEADER_LENGTH = 16
host = "127.0.0.1"
port = 5001  # initiate port no above 1024
client_list = []

def receive(socket):
    msg_hdr = socket.recv(HEADER_LENGTH) #read header
    msg_len = int(msg_hdr.decode('utf-8').strip()) #decode msg length
    msg_payload = socket.recv(msg_len) #read msg
    msg = msg_hdr + msg_payload
    print("Receive: " + str(msg))
    return msg

def broadcast(msg):
    print("broadcast")
    for client in client_list:
        client.send(msg)

def receive_handler(socket):
    while True:
        msg = receive(socket)
        broadcast(msg)

def chat(socket):
    print("autheticate")
    receive_thread = Thread(target = receive_handler, args = (socket,)) #receive msg from client program
    receive_thread.start()
    receive_thread.join()

def server_program():
    # get the hostname
    print(host)

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # queue up as many as 5 connect requests (the normal max) before refusing outside connections
    server_socket.listen(5)
    while True:
        client, cli_address = server_socket.accept()  # accept new connection
        print("Receive Connection Request from: " + str(cli_address))
        # receive data stream. it won't accept data packet greater than 1024 bytes
        client_list.append(client)
        Thread(target = chat, args = (client,)).start()




if __name__ == '__main__':
    server_program()