


import socket

LISTEN_IP = "0.0.0.0"  # naslouchat na všech rozhraních
PORT = 65432

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((LISTEN_IP, PORT))

print(f"Naslouchám na portu {PORT}...")

while True:
    data, addr = sock.recvfrom(1024)  # buffer 1024 bytů
    print(f"Přijato od {addr}: {data.decode()}")
    
    
    
    
    
    
    
    
    
    
    
    
    
    