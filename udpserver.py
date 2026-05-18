import socket
from message import Message
from response import Response

HOST = "localhost"
PORT = 12342



def run_udp_server(host=HOST, port=PORT):
    # Create a UDP socket (SOCK_DGRAM specifies UDP)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Bind the socket to the IP address and port
    server_socket.bind((host, port))
    print(f"UDP echo server listening on {host}:{port}")

    try:
        while True:
            # Wait for a message (up to 1024 bytes)
            rawbytes, client_address = server_socket.recvfrom(3)          
            message = bytearray(rawbytes)
            
            # Decode and print the received message
            print(f"Received '{message}' from {client_address}")
            
            message = Message(bytes=message)
            
            print(f'{message.respond}, {message.msgtype}, {message.version}, {message.temperature}')
            
            #server_header = Response("UPDATE_START", 2, []).header_b
            
           # server_socket.sendto(server_header, client_address)
            #print(f"Echoed message back to {client_address}\n")
            
    except KeyboardInterrupt:
        print("\nServer shutting down.")
    finally:
        # Always close the socket when done
        server_socket.close()
    
    

if __name__ == '__main__':
    run_udp_server()