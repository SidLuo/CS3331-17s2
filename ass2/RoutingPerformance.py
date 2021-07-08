import sys, os, time, random, heapq
import heapq

if len(sys.argv) != 6:
    sys.exit(sys.argv[0] + ": python NETWORK_SCHEME ROUTING_SCHEME TOPOLOGY_FILE WORKLOAD_FILE PACKET_RATE")

network_scheme = sys.argv[1]
assert network_scheme in ['CIRCUIT']
routing_scheme = sys.argv[2]
assert routing_scheme in ['SHP', 'SDP', 'LLP']
topology_file = sys.argv[3]
workload_file = sys.argv[4]
rate = int(sys.argv[5])

# read from file
try:
    file_read = open(topology_file, 'r')
    topology = file_read.read()
    file_read.close()
except IOexception:
    sys.exit("No such file! "+ topology_file)

try:
    file_read = open(workload_file, 'r')
    workload = file_read.read()
    file_read.close()
except IOexception:
    sys.exit("No such file! "+ workload_file)

if network_scheme == "CIRCUIT":
    edges = []
    connections = {}
    starts = []
    ends = []
    requests = {}
    if routing_scheme == "SHP":
        for line in topology:
            splitted = line.split()
            f = splitted[0]
            t = splitted[1]
            c = 1
            num = int(splitted[4])
            edges.append((f, t, c))
            connections[(f, c)] = num
        
        for line in workload:
            splitted = line.split()
            start = float(splitted[0])
            starts.append(start)
            requests[start] = [splitted[1], splitted[2], float(splitted[3])]
        # starting time
        start_time = time.time()
        while requests and ends:
            if starts[0] == time.time() - start_time:
                info = requests[starts[0]]
                ends.append(info[2])
                (cost, path) = dijkstra(edges, info[0], info[1])
                if cost == float("inf"):
                    sys.exit("No such file! "+ workload_file)
                else
                    for node in path:
                    if (
        
class Edge:
    def __init__(self, node1, node2, delay, capacity):
        self.from = node1
        self.to = node2
        self.delay = delay
        self.capacity = capacity
        self.load = 0
        
    def available(self):
        return self.capacity - self.load
        
class Node:
    def __init__(self):
        self.neighbours = []
    def add_neighbour(self, node):
        self.neighbours.append(node)
        
class Graph:
    def __init__(self):
        self.nodes = {}
        self.edges = {}
        self.circuits = {}
    def add_edge(self, node1, node2, delay, capacity):
        
        if node1 not in self.nodes:
            self.nodes[node1] = Node()
        
        edge = Edge(node1, node2, delay, capacity)
        self.edges[(sorted([node1, node2]))] = edge
        
    
class Circuit:
    def __init__
