import socket
from message import Message
from response import Response

HOST = "localhost"
PORT = 12342

def split_data(data, block_len):
    
    blocks_count = len(data)//block_len + (1 if len(data) % block_len > 0 else 0)
    data_list = []
    
    
    for i in range(blocks_count):
        if i*block_len
        data[i*(block_len):]

    return data_list
    

def send_blocks():
    pass  

def run_udp_server(host=HOST, port=PORT):
    # Create a UDP socket (SOCK_DGRAM specifies UDP)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Bind the socket to the IP address and port
    server_socket.bind((host, port))
    print(f"UDP echo server listening on {host}:{port}")
    #res = Response(msgtype="UPDATE_START", header_length=3, msg_id=1, data=b'helloworld')


    try:
        while True:
            # Wait for a message (up to 1024 bytes)
            rawbytes, client_address = server_socket.recvfrom(3)          
            message = bytearray(rawbytes)
            
            # Decode and print the received message
            print(f"Received '{message}' from {client_address}")
            
            message = Message(bytes=message)
            
            print(f'{message.respond}, {message.msgtype}, {message.version}, {message.temperature}')
            
            to_send = b'import socket'
            
            if message.respond == 1:
                res = Response(msgtype="UPDATE_START", header_length=4, block_id=200, data=to_send, block_len=len(to_send))            
                server_socket.sendto(res.header_byte, client_address)
                print(f"Echoed message back to {client_address}\n")
                if res.header_length > 0:
                    server_socket.sendto(res.header_ext_byte, client_address)
                    if res.block_len > 0:
                        server_socket.sendto(res.data, client_address)
            
    except KeyboardInterrupt:
        print("\nServer shutting down.")
    finally:
        # Always close the socket when done
        server_socket.close()
    
    

if __name__ == '__main__':
    run_udp_server()
    
