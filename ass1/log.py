# COMP3331 Assignment1
# Author: Guozhao Luo

import sys, time, packet

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

# record log
def record(file_name, status, packet, start_time):
    flag = ""
    if (packet.get_flag() == SYN):
        flag = "S"
    elif (packet.get_flag() == SYN_ACK):
        flag = "SA"
    elif (packet.get_flag() == NULL):
        flag = "D"
    elif (packet.get_flag() == FIN):
        flag = "F"
    elif (packet.get_flag() == FIN_ACK):
        flag = "FA"
    elif (packet.get_flag() == ACK):
        flag = "A"
    # actn  time    flag seq   bytes ack 
    # snd   34.335  S    121   0     0
    # rcv   34.4    SA   154   0     122
    # snd   34.54   A    122   0     155
    # snd   34.57   D    122   56    155
    # drop  34.67   D    178   56    155
    try:
        file = open(file_name, 'a')
        file.write('%4s %3.3f %2s %4d %3d %4d\n' % (status, time.time() - start_time,
                     flag, packet.get_seq_num(), len(packet.unpack()), packet.get_ack_num()))
        file.close()
    except:
        sys.exit("An error occurred trying to write to the file " + file_name)
       
       
# generate statistics for receiver
def receiver_data(file_name, last_received, segments, total):
    print ("printing statistics")
    try:
        file = open(file_name, 'a')
        file.write("\n\nStatistics\n")
        file.write("Bytes received:       " + str(last_received) + "\n")
        file.write("Segments received:    " + str(segments) + "\n")
        file.write("Duplicate segments:   " + str(total) + "\n")
        file.close()
    except:
        sys.exit("An error occurred trying to write to the file " + file_name)
