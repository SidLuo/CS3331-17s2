# COMP3331 Assignment1
# Author: Guozhao Luo

import sys, time, datetime, random, collections, socket, glob, log
import packet

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

if len(sys.argv) != 9:
    sys.exit(sys.argv[0] + ": python receiver_host_ip receiver_post file MWS MSS timeout pdrop seed")

state = CLOSED

receiver_host_ip = sys.argv[1]
receiver_port = int(sys.argv[2])
file_name = sys.argv[3]
mws = int(sys.argv[4])
mss = int(sys.argv[5])
timeout = float(sys.argv[6])
pdrop = float(sys.argv[7])
seed = int(sys.argv[8])

# random generate
random.seed(seed)

# starting time
start_time = time.time()

# initialized log
log_file = 'Sender_log.txt'
glob.glob(log_file)

sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sender.settimeout(timeout/1000)

# handshake
if state == CLOSED:
    p = packet.Packet(SYN)

    sender.sendto(str(p.get_list()), (receiver_host_ip, receiver_port))
    log.record(log_file, "snd", p, start_time)
    state = LISTEN
    print "handshake sent"
    try:
        response = sender.recv(1024)
        p = packet.Packet(NULL)
        p.parse(response)
        log.record(log_file, "rcv", p, start_time)

        if p.get_flag() == SYN_ACK:
            state = ESTABLISHED
            p = packet.Packet(ACK)
            p.set_seq(1)
            p.set_ack(1)
            sender.sendto(str(p.get_list()), (receiver_host_ip, receiver_port))
            print "connected to " + receiver_host_ip + ":" + str(receiver_port)
        else:
            sys.exit("handshake error: unexpected response " + response)
    except socket.timeout:
        sys.exit("handshake error: time out")
        
# read from file
try:
    file_read = open(file_name, 'r')
    file = file_read.read()
    file_read.close()
except IOexception:
    sys.exit("No such file! "+ file_name)
window = []
head = 0
next = 0
file_sent = False
acks = []
while not file_sent:
    next = head + mss * len(window)

    while len(window) < mws/mss and next < len(file):
        # window not full, put new packets in
        p = packet.Packet(NULL)
        p.set_seq(next)
        if next + mss < len(file):
            p.pack(file[next:next + mss])
            next = next + mss
        else:
            p.pack(file[next:])
            next = len(file)
        drop = random.random()
        if drop > pdrop:
            sender.sendto(str(p.get_list()), (receiver_host_ip, receiver_port))
            print "packet sent: " + str(p.get_seq_num())
            log.record(log_file, "snd", p, start_time)
        else:
            print "datagram dropped"
            log.record(log_file, "drop", p, start_time)
        window.append(p)
        
    
    try:
        response, receiver = sender.recvfrom(1024)
        p = packet.Packet(NULL)
        p.parse(response)
        log.record(log_file, "rcv", p, start_time)
        print response
        if p.get_flag() == ACK:
            ack = p.get_ack_num()
            if ack >= len(file):
                file_sent = True
                print "last data ACK received"
            else:
                # move the window by removing every segment smaller than ACK
                for x in window:
                    if x.get_seq_num() < ack:
                        window.remove(x)
                head = ack
                # fast retrainsmit
                acks.append(ack)
                counter = collections.Counter(acks)
                if counter[ack] > 3:
                    print "fast retrainsmit: ack = " + str(ack)
                    p = packet.Packet(NULL)
                    p.set_seq(ack)
                    p.pack(file[ack:ack + mss])
                    drop = random.random()
                    if drop > pdrop:
                        sender.sendto(str(p.get_list()), (receiver_host_ip, receiver_port))
                        log.record(log_file, "snd", p, start_time)
                    else:
                        print "Datagram dropped"
                        log.record(log_file, "drop", p, start_time)

        else:
            print "error: received non-ack"
    except socket.timeout:
        print "time out, resending..."
        for p in window:
            drop = random.random()
            if drop > pdrop:
                sender.sendto(str(p.get_list()), (receiver_host_ip, receiver_port))
                log.record(log_file, "snd", p, start_time)
            else:
                print "datagram dropped"
                log.record(log_file, "drop", p, start_time)
    
# teardown
if state == ESTABLISHED:
    p = packet.Packet(FIN)
    p.set_seq(0)
    p.set_ack(0)
    
    sender.sendto(str(p.get_list()), (receiver_host_ip, receiver_port))
    state = FIN_WAIT
    log.record(log_file, "snd", p, start_time)

    while state != CLOSED:
        try:
            response = sender.recv(1024)
            p = packet.Packet(NULL)
            p.parse(response)
            log.record(log_file, "rcv", p, start_time)
            
            # received FIN_ACK, update state
            if state == FIN_WAIT and p.get_flag() == FIN_ACK:
                state = CLOSING
            # received FIN, send FIN_ACK and update state to CLOSED
            elif state == CLOSING and p.get_flag() == FIN:
                p = packet.Packet(FIN_ACK)
                p.set_seq(0)
                p.set_ack(0)
                sender.sendto(str(p.get_list()), (receiver_host_ip, receiver_port))
                log.record(log_file, "snd", p, start_time)
                state = CLOSED
                print "received last FIN"
            else:
                print "teardown error: unexpected response " + response
        except socket.timeout:
            print "teardown error: time out"

sys.exit("done, bye! :)")
