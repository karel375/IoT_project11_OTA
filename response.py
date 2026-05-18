MSGTYPE_MASK = 0b01110000
HEADER_SIZE_MASK = 0b00001111

BYTE_MASK = 0b11111111

# Standardized to match the Message style: {int: "STRING"}
server_msg_types = {3: "UPDATE_START", 4: "NO_UPDATE", 5: "DATA_BLOCK"}
server_msg_types_rev = {v: k for k, v in server_msg_types.items()}

class Response:
    """
    fields:
    header - int representation of header
    header_b - bytes object representation of header
    
    msgtype - string, flag
    header_length - int, flag
    
    header_ext - list of int representations of extended header bytes
    header_ext_b - byte object representation of extended header
    
    message_id - int, extended header info
    block_len - int, extended header info, no. of bytes to be sent
    
    data_b
    """

    
    def __init__(self, header=None, msgtype="UPDATE_START", header_length=1, msg_id=0, block_len=1024, data=None):
        # Initialize instance-specific data list
        self.data = data if data is not None else []
        
        if header is not None: # client side -> decode from received data
            # ==========================================
            # DECODE MODE: Initialize from a single byte
            # ==========================================
            self.header = header
            self.header_b = self.header.to_bytes(1, byteorder='big')
            
            # Extract the 3 bits for message type
            msg_val = (header & MSGTYPE_MASK) >> 4
            self.msgtype = server_msg_types.get(msg_val, "INVALID")
            
            # Extract the 4 bits for header length
            self.header_length = header & HEADER_SIZE_MASK
            
        else:
            # ==========================================
            # ENCODE MODE: Initialize from flags/fields
            # ==========================================
            self.msgtype = msgtype
            self.header_length = header_length if header_length < 16 else 0
            self.header = 0
            self.header_b = b''
            self.header_encode()

    def edit_header(self, msgtype, header_length):
        """Allows updating the header fields and re-encoding the binary header."""
        self.msgtype = msgtype
        self.header_length = header_length if header_length < 16 else 0
        self.header_encode()

    def header_encode(self):
        """Encodes the current string msgtype and header_length into the binary header."""
        # 1. Look up the integer value for the string msgtype, default to 0 if invalid
        msg_val = server_msg_types_rev.get(self.msgtype, 0)
        msg_bits = (msg_val << 4) & MSGTYPE_MASK
        
        # 2. Ensure header_length doesn't exceed its allocated 4 bits
        len_bits = self.header_length & HEADER_SIZE_MASK
        
        # 3. Combine them using bitwise OR
        self.header = msg_bits | len_bits
        
        # 4. Create the bytes representation (1 byte long, big-endian)
        self.header_b = self.header.to_bytes(1, byteorder='big')
    
    def extend_header(self, header_ext_b):
        self.header_ext_b = header_ext_b # list
        self.header_ext = []
        
        for i in len(self.header_ext_b):
            self.header_ext[i] = int.from_bytes(header_ext_b[i])
        
        self.message_id = self.header_ext[0] << 8 + self.header_ext[1]
        self.block_len = self.header_ext[2] << 8 + self.header_ext[3]
        
        
             
            
        
            

    def __repr__(self):
        return f"<Response header={bin(self.header)} msgtype='{self.msgtype}' header_length={self.header_length}>"