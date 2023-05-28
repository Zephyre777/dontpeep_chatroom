import socket
import sys
import threading
from threading import Thread
from utils import Client
import time

HEADER_LENGTH = 16

def send(msg, socket, encrypted): #generate header and send msg
    if(not encrypted):
        msg = str(msg).encode('utf-8')

    msg_hdr = f"{len(msg):<{HEADER_LENGTH}}".encode('utf-8') #left-align with length [HEADER_LENGTH]

    #send the utf-8 encoded msg
    print("Send: " + str(msg, "utf-8"))
    socket.send(msg_hdr+msg)
    
def receive(socket):
    #read msg
    msg_hdr = socket.recv(HEADER_LENGTH) #read header
    msg_len = int(msg_hdr.decode('utf-8').strip()) #decode msg length
    msg_payload = socket.recv(msg_len) #read msg
    msg = msg_hdr + msg_payload
    print("Receive: " + str(msg_payload, "utf-8"))
    return msg_payload
    # msg = socket.recv(msg_len) 
    # if(msg_type == 'e'): #Msg is encrypted
    #     print("Receive: " + str(msg))
    # elif(msg_type == 'r'):
    #     client = Client(int(msg.decode('utf-8').strip())) #Initialize Client with p
    
def send_handler(socket):
    print("Type in your message")
    while True:
        msg = input("\n>")
        if(msg == "quit"):
            break
        encrypted = False
        send(msg, socket, encrypted)
        time.sleep(0.05)
    socket.close()

def receive_handler(socket, event):
    while True:
        if event.is_set():
            break
        receive(socket)

def initialization(socket):
    print("Please type in your username")
    userName = input("\n>")
    send(userName, socket, 0)
    global client
    client = Client(int.from_bytes(receive(socket)))
    send(client.publicKey, socket, 0)
    
def client_program(ip, port):
    client_socket = socket.socket() #create a client socket instance
    client_socket.connect((IP_address, Port))  

    initialization(client_socket)
    event = threading.Event()

    send_thread = Thread(target = send_handler, args = (client_socket,)) #send msg thread
    receive_thread = Thread(target = receive_handler, args = (client_socket,event, )) #receive msg from server program
    send_thread.start()
    receive_thread.start()

    send_thread.join()
    receive_thread.set()

if __name__ == '__main__':
    #Check input correctness
    if len(sys.argv) != 3:
        print ("Input parameters incorrect. Expecting [IP address, port number]")
        exit()
    
    IP_address = str(sys.argv[1])
    Port = int(sys.argv[2])
    
    global client
    client_program(IP_address, Port)
    
