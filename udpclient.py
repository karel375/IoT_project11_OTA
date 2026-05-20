import socket
from message import Message
from response import Response


host = '127.0.0.1'
port = 12342

# Create a UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

message = Message(respond=True, msgtype="POLL", version=3, temperature=24.44)

try:
    # Send data
    print(f"Sending: '{message}'")
    client_socket.sendto(message.msg_byte, (host, port))
    
    header, server = client_socket.recvfrom(1)
    print(f"Received: '{bin(header[0])}' from {server}")
    
    resp = Response(header=header[0])
    print(f"{resp.msgtype} {resp.header_length}")
    if (resp.header_length > 0):
        ext_header, server = client_socket.recvfrom(resp.header_length)
        resp.extend_header(ext_header)
        print(f"ID: {resp.block_id}, len: {resp.block_len}, bytes: {ext_header}")
        
        data_block, server = client_socket.recvfrom(resp.block_len)
        
        with open("fw_new.py", "wb") as file:
            file.write(data_block)
            

    
finally:
    client_socket.close()
