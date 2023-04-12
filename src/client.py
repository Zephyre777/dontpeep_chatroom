import socket
import sys
from threading import Thread

HEADER_LENGTH = 16

def send(msg, socket, encrypted): #generate header and send msg
    if(not encrypted):
        msg = msg.encode('utf-8')

    msg_hdr = f"{len(msg):<{HEADER_LENGTH}}".encode('utf-8') #left-align with length [HEADER_LENGTH]

    #send the utf-8 encoded msg
    print("Send: " + str(msg))
    socket.send(msg_hdr+msg)
    
def receive(socket):
    msg_hdr = socket.recv(HEADER_LENGTH) #read header
    msg_len = int(msg_hdr.decode('utf-8').strip()) #decode msg length
    msg = socket.recv(msg_len) #read msg
    print("Receive: " + str(msg))

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

    client_program(IP_address, Port)
    
