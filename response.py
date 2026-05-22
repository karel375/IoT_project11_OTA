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
    header_byte
    
    msgtype - string, flag
    header_length - int, flag
    
    header_ext - list of int representations of extended header bytes
    header_ext_byte
    
    block_id - int, extended header info
    block_len - int, extended header info, no. of bytes to be sent
    
    resp_byte - bytearray representation of the entire response
    
    data - bytearray of block
    """

    
    def __init__(self, header=None, msgtype=None, header_length=0, block_id=None, block_len=1024, data=None):
        # Initialize instance-specific data list
        self.data = data if data is not None else bytearray()
        
        if header is not None: # client side -> decode from received data
            # ==========================================
            # DECODE MODE: Initialize from a single byte
            # ==========================================
            
            # shitty cast byte to int
            self.header = bytearray(header)[0]
            
            # Extract the 3 bits for message type
            msgtype_val = (self.header & MSGTYPE_MASK) >> 4
            self.msgtype = server_msg_types.get(msgtype_val, "INVALID")
            
            # Extract the 4 bits for header length
            self.header_length = self.header & HEADER_SIZE_MASK
            
        else:
            # ==========================================
            # ENCODE MODE: Initialize from flags/fields
            # ==========================================
            self.msgtype = msgtype
            self.header_length = header_length if header_length < 16 else 0
            self.header = 0            
            """Encodes the current string msgtype and header_length into the binary header."""
            # 1. Look up the integer value for the string msgtype, default to 0 if invalid
            msgtype_val = server_msg_types_rev.get(self.msgtype, 0)
            msgtype_int = (msgtype_val << 4) & MSGTYPE_MASK
            
            # 2. Ensure header_length doesn't exceed its allocated 4 bits
            ext_header_len_bits = self.header_length & HEADER_SIZE_MASK

            self.header_byte = bytearray([msgtype_int | ext_header_len_bits])
            
            if (self.header_length > 0) :
                self.block_id = block_id
                self.block_len = block_len
                block_id_upper = block_id >> 8
                block_id_lower = block_id & 0xFF
                
                block_len_upper = block_len >> 8
                block_len_lower = block_len & 0xFF
                self.header_ext_byte = bytearray([block_id_upper, block_id_lower, block_len_upper, block_len_lower])
                print(self.header_ext_byte)
                


    def extend_header(self, header_ext):
        self.header_ext = header_ext
        
        self.block_id = (header_ext[0] << 8) | header_ext[1]
        self.block_len = (header_ext[2] << 8) | header_ext[3]
    
    def edit_header(self, msgtype, header_length):
        """Allows updating the header fields and re-encoding the binary header."""
        self.msgtype = msgtype
        self.header_length = header_length if header_length < 16 else 0
        self.header_encode()
   
    def __repr__(self):
        return f"<Response header={bin(self.header)} msgtype='{self.msgtype}' header_length={self.header_length}>"