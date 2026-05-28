import usocket as socket
import uhashlib as hashlib
import machine
import neopixel
import os
import time

from message import Message
from response import Response

import BG77

host = '147.229.148.105'
port = 7008
pathto = 'C:\\Users\\marti\\Documents\\GitHub\\IoT_project11_OTA\\'

def register_module(module):
    module.setRadio(0)
    time.sleep(1)
    module.setRadio(1)
    module.setAPN("lpwa.vodafone.iot")
    return module.attachToNetwork()

def open_socket(module):
    if module.isRegistered():
        result, sock = module.socket(BG77.AF_INET, BG77.SOCK_DGRAM)
        sock.settimeout(5)
        if not result:
            print("Failed to open UDP socket")
            return False, None
        else:
            sock.connect(ip=host, remote_port=port)
            return True, sock
    else:
        print("ERROR, module not connected to network")
        
def is_sleeping():
    return False

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




bg_uart = machine.UART(0, baudrate=115200, tx=machine.Pin(0), rxbuf=256, rx=machine.Pin(1), timeout = 0, timeout_char=1)
module = BG77.BG77(bg_uart, verbose=True, radio=False)
at_ok = module.testAT()

print("AT OK" if module.testAT() else "AT ERROR")


register_module(module)

print("Attached" if register_module(module) else "Failed to attach")

module.sendCommand("AT+QCSCON=1\r\n")



# Create a UDP socket


#############
# Main loop #
#############



try:
    # Send message with temp and expect response
    poll_count = 0
    poll_max = 2
    
    curr_ticks = time.ticks_ms()
    tick_interval = 1000
    
    
    message = Message(respond=True, msgtype="POLL", version=2, temperature=24.44)
    
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


