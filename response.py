MSGTYPE_MASK = (0b01110000)
HEADER_SIZE_MASK = (0b00001111)

server_msg_types = {"UPDATE_START": 3, "NO_UPDATE": 4, "DATA_BLOCK": 5}

class Response():
    
    header = 0b0
    
    msgtype = 3
    header_length = 1
    data = []
    
    def __init__(self, msgtype, header_length, data):
        self.msgtype = server_msg_types[msgtype]
        self.header_length = header_length if (header_length < 16) else 0
        self.data = data
        self.header_encode()
        
    def edit_header(self, msgtype, header_length):
        self.msgtype = server_msg_types[msgtype]
        self.header_length = header_length if (header_length < 16) else 0
        self.header_encode()
    
    def header_encode(self):
        self.header = self.header | (self.msgtype << 4)
        self.header = self.header | (self.header_length)
        self.header_b = int.to_bytes(self.header)

            