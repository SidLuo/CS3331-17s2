# COMP3331 Assignment1
# Author: Guozhao Luo

import sys, os, time, glob
import packet, log

from socket import *

# flags
NULL = 0
FIN = 1
SYN = 2
FIN_SYN = 3
ACK = 10
FIN_ACK = 11
SYN_ACK = 12
FIN_SYN_ACK = 13

CLOSED = 0
LISTEN = 1
ESTABLISHED = 2
FIN_WAIT = 3
CLOSING = 4

if len(sys.argv) != 3:
    sys.exit(sys.argv[0] + ": python receiver_port file")

# write to file
def write_file(buffer):
    try:
        file = open(file_name, 'a')
        file.write(buffer)
        file.close()
    except:
        sys.exit("An error occurred trying to write to the file " + file_name)
        
        
        
state = CLOSED

receiver_host_ip = "localhost"
receiver_port = int(sys.argv[1])
file_name = sys.argv[2]

receiver = socket(AF_INET, SOCK_DGRAM)
receiver.bind((receiver_host_ip, receiver_port))

# initiate variables
last_received = 0
total = 0
segments = 0

# initialized log
log_file = 'Receiver_log.txt'
glob.glob(log_file)

# starting time
start_time = time.time()

while True:
    data, sender = receiver.recvfrom(receiver_port)
    p = packet.Packet(NULL)
    p.parse(data)
    
    log.record(log_file, "rcv", p, start_time)
    # get host and port
    sender_host = sender[0]
    sender_port = sender[1]
    if state == CLOSED:
        
        if p.get_flag() == SYN:
            p = packet.Packet(SYN_ACK)
            p.set_ack(0)
            p.set_seq(1)
            receiver.sendto(str(p.get_list()), (sender_host, sender_port))
            
            log.record(log_file, "snd", p, start_time)

            state = LISTEN

            print "listening to " + sender_host +":" + str(sender_port)
        else:
            sys.exit("error: not SYN" + data + p.get_flag())
    elif state == LISTEN:
        if p.get_flag() == ACK:
            state = ESTABLISHED
            glob.glob(file_name)
            print "connected to " + sender_host +":" + str(sender_port)

    elif state == ESTABLISHED:
        # received data segments
        if p.get_flag() == NULL:
            total += 1
            buffer = p.unpack()
            seq_num = p.get_seq_num()
            
            # generate ACK
            if seq_num == last_received:
                segments += 1
                p = packet.Packet(ACK)
                p.set_ack(seq_num + len(buffer))
                receiver.sendto(str(p.get_list()), (sender_host, sender_port))
                log.record(log_file, "snd", p, start_time)

                last_received = seq_num + len(buffer)

                write_file(buffer)
            elif seq_num > last_received:
                print "packet lost"
                p = packet.Packet(ACK)
                p.set_ack(last_received)
                receiver.sendto(str(p.get_list()), (sender_host, sender_port))
                log.record(log_file, "snd", p, start_time)
            #else:
                # duplicated
                
                
        # received FIN, start disconnecting
        if p.get_flag() == FIN:
            print "disconnecting: sending FIN_ACK"

            p = packet.Packet(FIN_ACK)
            receiver.sendto(str(p.get_list()), (sender_host, sender_port))
            log.record(log_file, "snd", p, start_time)

            state = CLOSING

            p = packet.Packet(FIN)
            receiver.sendto(str(p.get_list()), (sender_host, sender_port))
            log.record(log_file, "snd", p, start_time)
    elif state == CLOSING:
        if p.get_flag() == FIN_ACK:
            state = CLOSED
            log.receiver_data(log_file, last_received, segments, total)
            sys.exit("disconnected: last ACK received.")
