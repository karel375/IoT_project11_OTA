REPLY_MASK = (0b10000000)
MSGTYPE_MASK = (0b01110000)
VERSION_MASK = (0b00001111)

client_msg_types = {0: "POLL", 1: "ACK", 2: "NACK"}

class Message():
    
    header = 0b0
    
    respond = False
    msgtype = ""
    version = 0
    data = []
    
    def __init__(self, header):
        self.header = header
        self.respond = True if ((header & REPLY_MASK) >> 7) == 1 else False
        self.msgtype = "INVALID" if ((header & MSGTYPE_MASK >> 4) > 2) else client_msg_types[(header & MSGTYPE_MASK >> 4)]
        self.version = header & VERSION_MASK
    
    def add_data(self, data_byte):
        self.data.append(data_byte)
            