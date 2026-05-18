REPLY_MASK = 0b10000000
MSGTYPE_MASK = 0b01110000
VERSION_MASK = 0b00001111

client_msg_types = {0: "POLL", 1: "ACK", 2: "NACK"}
# Reverse lookup dictionary for encoding ("POLL" -> 0, etc.)
client_msg_types_rev = {v: k for k, v in client_msg_types.items()}

class Message:
    def __init__(self, header=None, respond=False, msgtype="POLL", version=0):
        # Initialize instance variables
        self.data = []
        
        if header is not None:
            # ==========================================
            # DECODE MODE: Initialize from a single byte
            # ==========================================
            self.header = header
            self.respond = bool((header & REPLY_MASK) >> 7)
            
            # Extract the 3 bits for message type (Fixed precedence with parentheses)
            msg_val = (header & MSGTYPE_MASK) >> 4
            self.msgtype = client_msg_types.get(msg_val, "INVALID")
            
            self.version = header & VERSION_MASK
            
        else:
            # ==========================================
            # ENCODE MODE: Initialize from flags/fields
            # ==========================================
            self.respond = respond
            self.msgtype = msgtype
            self.version = version
            
            # 1. Shift the boolean respond value to the 7th bit
            reply_bits = (1 if respond else 0) << 7
            
            # 2. Look up the integer value for the string msgtype, default to 7 (Invalid)
            msg_val = client_msg_types_rev.get(msgtype, 0b111)
            msg_bits = (msg_val << 4) & MSGTYPE_MASK
            
            # 3. Ensure version doesn't exceed its allocated 4 bits
            ver_bits = version & VERSION_MASK
            
            # Combine them using bitwise OR to create the header
            self.header = reply_bits | msg_bits | ver_bits

    def add_data(self, data_byte):
        self.data.append(data_byte)

    def __repr__(self):
        return f"<Message header={bin(self.header)} respond={self.respond} msgtype='{self.msgtype}' version={self.version}>"