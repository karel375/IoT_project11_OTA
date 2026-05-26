import socket
from message import Message
from response import Response
import hashlib

HOST = "localhost"
PORT = 12342
CURRENT_VERSION = 3

def split_data(data, block_len):
    
    blocks_count = len(data)//block_len + (1 if len(data) % block_len > 0 else 0)
    data_list = []
    
    
    for i in range(blocks_count):
        data_list.append(data[i*block_len:(i+1)*block_len]) 

    return data_list
    
"""
sock - socket object of client
client - socket object from recvfrom
data - bytearray of the entire payload
block_len - int bytes per block
"""
def send_payload(sock, client, data, block_len):
    data_list = split_data(data, block_len) # turn into list of bytearrays of block_len size each
    
    if len(data_list) == 0:
        res = Response(msgtype="NO_UPDATE")
    else:
        res = Response(msgtype="UPDATE_START")
    sock.sendto(res.header_byte, client)
    
    if len(data_list) == 0:
        return False
    
    rawbytes, client = sock.recvfrom(1)
    
    msg = Message(bytes=rawbytes)
    
    if (msg.msgtype != "ACK"):
        return False
        
     
    for i in range(len(data_list)):
        data_block = Response(msgtype="DATA_BLOCK", header_length=4, block_len=len(data_list[i]), data=data_list[i], block_id=i)
        
        # send header
        sock.sendto(data_block.header_byte, client)
    
        # send extended header
        sock.sendto(data_block.header_ext_byte, client)
        
        rawbytes, client = sock.recvfrom(1)
        msg = Message(bytes=rawbytes)
        if (msg.msgtype != "ACK"):
            return False
        
        # send data block
        sock.sendto(data_block.data, client)
        
    eot = Response(msgtype="NO_UPDATE")
    sock.sendto(eot.header_byte, client)
    return True


    

def run_udp_server(host=HOST, port=PORT):
    # Create a UDP socket (SOCK_DGRAM specifies UDP)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Bind the socket to the IP address and port
    sock.bind((host, port))
    print(f"UDP echo server listening on {host}:{port}")


    try:
        while True:
            # Wait for a message (up to 1024 bytes)
            rawbytes, client = sock.recvfrom(3)          
            message = bytearray(rawbytes)
            
            # Decode and print the received message
            print(f"Received '{message}' from {client}")
            
            message = Message(bytes=message)
            
            print(f'{message.respond}, {message.msgtype}, {message.version}, {message.temperature}')
                        
            if message.respond == 1:
                if message.version != CURRENT_VERSION and message.msgtype == "POLL":
                    with open('C:\\Users\\marti\\Documents\\GitHub\\IoT_project11_OTA\\dummy_fw.py', 'rb') as fw:
                        payload = fw.read()

                    hash = hashlib.sha256()
                    hash.update(payload)
                    hashstring = hash.hexdigest()
                    send_payload(sock, client, payload, 1024)
                    send_payload(sock, client, bytearray(hashstring, 'utf-8'), 32)
                else:
                    res = Response(msgtype="NO_UPDATE", header_length=0)
                    sock.sendto(res.header_byte, client)


    except KeyboardInterrupt:
        print("\nServer shutting down.")
    finally:
        # Always close the socket when done
        sock.close()
    
    

if __name__ == '__main__':
    run_udp_server()
    
