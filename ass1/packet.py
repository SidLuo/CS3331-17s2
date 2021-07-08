# COMP3331 Assignment1
# Author: Guozhao Luo

import ast

# defines
ACK_NUM = 0
SEQ_NUM = 1
FLAG = 2
DATA = 3

# An object that represents a packet in STp protocol
class Packet:
    # creates a packet and initiate a list
    def __init__(self, flag):
        self.list = [0, 0, 0, 0]
        self.flag = flag
        self.list[FLAG] = flag
    
    # receive a list and parse it
    def parse(self, list):
        self.list = ast.literal_eval(list)
        self.flag = self.list[FLAG]
        self.seq_num = self.list[SEQ_NUM]
        self.ack_num = self.list[ACK_NUM]
        
    def set_seq(self, seq):
        self.seq = seq
        self.list[SEQ_NUM] = seq

    def set_ack(self, ack):
        self.ack = ack
        self.list[ACK_NUM] = ack
        
    def get_flag(self):
        return self.flag
        
    def get_ack_num(self):
        return self.list[ACK_NUM]
        
    def get_seq_num(self):
        return self.list[SEQ_NUM]
    
    def get_list(self):
        return self.list

    # append the data at the end of the list
    def pack(self, data):
        self.list[DATA] = data

    # get the data
    def unpack(self):
        return str(self.list[DATA])
