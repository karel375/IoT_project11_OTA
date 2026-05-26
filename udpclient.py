import socket
from message import Message
from response import Response
import hashlib


host = '127.0.0.1'
port = 12342
pathto = 'C:\\Users\\marti\\Documents\\GitHub\\IoT_project11_OTA\\'

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

message = Message(respond=True, msgtype="POLL", version=4, temperature=24.44)

def recv_write_payload(sock, filename):
    
    payload_str = ""
    
    # erase previous temp file
    with open(pathto + filename, "wb") as file:
        file.write(b'')
    
    expected_id = 0
    while True:
        # get first header byte    
        rawbytes = sock.recv(1)
        resp = Response(header=rawbytes)
        
        if (resp.msgtype == "NO_UPDATE"):
            break
        
        # get extended header
        rawbytes = sock.recv(resp.header_length)
        resp.extend_header(rawbytes)
        
        print(f'{resp.block_id}, {resp.block_len}')
        
        if (resp.block_id != expected_id):
            # send NACK when the counter does not match
            nack = Message(respond=True, msgtype="NACK")
            sock.sendto()
            
            # try to receive the block again
            continue
        
        ack = Message(respond=True, msgtype="ACK")
        sock.sendto(ack.msg_byte, (host, port))
        
        rawbytes = sock.recv(resp.block_len)
        payload_str += rawbytes.decode("utf-8")
        with open(pathto + filename, 'ab') as file:
            file.write(rawbytes)    
            

        expected_id += 1
        
    return payload_str

#############
# Main loop #
#############
try:
    # Send message with temp and expect response
    print(f"Sending: '{message}'")
    sock.sendto(message.msg_byte, (host, port))
    
    if (message.respond):    
        # receive header
        rawbytes = sock.recv(1)
        
        print(f"Received: '{bin(rawbytes[0])}'")
        
        # Decode 1st header byte
        resp = Response(header=rawbytes)
        print(f"{resp.msgtype} {resp.header_length}")
        
        # update procedure
        if resp.msgtype == "UPDATE_START":
            # send ack to start update
            ack = Message(respond=True, msgtype="ACK")
            sock.sendto(ack.msg_byte, (host, port))
            
            payload = recv_write_payload(sock, "new_fw.py")
            
            # wait for SHA checksum receipt
            rawbytes = sock.recv(1)
            resp = Response(header=rawbytes)
        
            if (resp.msgtype == "UPDATE_START"):
                ack = Message(respond=True, msgtype="ACK")
                sock.sendto(ack.msg_byte, (host, port))
                sha = recv_write_payload(sock, "shasum")
                sha_new = hashlib.sha256()
                sha_new.update(bytearray(payload, 'utf-8'))
                sha_new_str = sha_new.hexdigest()
                print(f"RCVD: {sha}, CALC:{sha_new_str}")
                
                       
            else:
                print("failed update")

        elif (resp.msgtype == "NO_UPDATE"):
            print("nothing to update")

        
        # If there is an extended header (header_length > 0), receive and decode
        if (resp.header_length > 0):
            ext_header, server = sock.recvfrom(resp.header_length)
            
            # add extended header to object
            resp.extend_header(ext_header)
            print(f"ID: {resp.block_id}, len: {resp.block_len}, bytes: {ext_header}")
            
            
            data_block, server = sock.recvfrom(resp.block_len)
            
            with open("fw_new.py", "wb") as file:
                file.write(data_block)
except KeyboardInterrupt:
    print("smrt")
    exit()
    
finally:
    sock.close()
