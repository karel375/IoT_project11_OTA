import socket

host = '127.0.0.1'
port = 12345

# Create a UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

message = 0b10100010

try:
    # Send data
    print(f"Sending: '{message}'")
    client_socket.sendto(message.to_bytes(1, 'big'), (host, port))
    
    header, server = client_socket.recvfrom(1)
    data = int.from_bytes(header)
    print(f"Received: '{bin(data)}' from {server}")
    
finally:
    client_socket.close()
