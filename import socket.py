import socket


HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

message = ''
data_size = 2

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((HOST, PORT))



def send(message):
    s.sendto(message, (HOST, PORT))


'''
Header: 
b1: 1 - respond, 0 - do not respond
b2: 


'''




while True:
    data = s.recv(data_size)

    
    print("Message: ", data)
















