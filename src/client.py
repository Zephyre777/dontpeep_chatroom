import socket
import sys
from threading import Thread
from utils import Client

HEADER_LENGTH = 16

def send(msg, socket, encrypted): #generate header and send msg
    if(not encrypted):
        msg = msg.encode('utf-8')

    msg_hdr = f"{len(msg):<{HEADER_LENGTH}}".encode('utf-8') #left-align with length [HEADER_LENGTH]

    #send the utf-8 encoded msg
    print("Send: " + str(msg))
    socket.send(msg_hdr+msg)
    
def receive(socket):
    #read msg type
    msg_hdr_type = socket.recv(1) 
    msg_type = str(msg_hdr_type) #decode msg length

    #read header
    msg_hdr = socket.recv(HEADER_LENGTH) 
    msg_len = int(msg_hdr.decode('utf-8').strip()) #decode msg length

    #read msg
    msg = socket.recv(msg_len) 
    if(msg_type == 'e'): #Msg is encrypted
        print("Receive: " + str(msg))
    elif(msg_type == 'r'):
        client = Client(int(msg.decode('utf-8').strip())) #Initialize Client with p
    

def send_handler(socket):
    print("Type in your message")
    while True:
        msg = input("\n>")
        encrypted = False
        send(msg, socket, encrypted)


def receive_handler(socket):
    while True:
        receive(socket)



def client_program(ip, port):
    client_socket = socket.socket() #create a client socket instance
    client_socket.connect((IP_address, Port))  
    send_thread = Thread(target = send_handler, args = (client_socket,)) #send msg thread
    receive_thread = Thread(target = receive_handler, args = (client_socket,)) #receive msg from server program

    send_thread.start()
    receive_thread.start()

    send_thread.join()
    receive_thread.join()


if __name__ == '__main__':
    #Check input correctness
    if len(sys.argv) != 3:
        print ("Input parameters incorrect. Expecting [IP address, port number]")
        exit()
    
    IP_address = str(sys.argv[1])
    Port = int(sys.argv[2])
    
    global client
    client_program(IP_address, Port)
    
