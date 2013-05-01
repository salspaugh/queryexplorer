#!/usr/bin/env python

import json
#import numpy as np
import sys

#from queryexplorer import connect_db

CSV_FILENAME = '/Users/salspaugh/queryexplorer/data/unique_args.csv'
#EDGES_FILE = '/Users/salspaugh/queryexplorer/data/args_adjacency_list_all.txt'
#EDGES_FILE = '/Users/salspaugh/queryexplorer/data/args_adjacency_list_short.txt'
#EDGES_FILE = '/Users/salspaugh/queryexplorer/data/test.txt'
EDGES_FILE = '/data/deploy/boss/data/args_adjacency_list_all.txt'

#NUM_ARGS = 41713. # number of unique args

class Node(object):

    def __init__(self, id):
        self.id = id
        self.neighbors = set()

    def __eq__(self, other):
        return self.id == other.id

    def __repr__(self):
        return 'id: ' + str(self.id) + ', neighbors: ' + str([n.id for n in self.neighbors])

    def connected(self, other):
        return other in self.neighbors

class Clique(object):
    
    def __init__(self):
        self.nodes = set()

    def __eq__(self, other):
        return len(self.nodes ^ other.nodes) == 0

    def __repr__(self):
        return 'nodes: ' + str([n.id for n in self.nodes])

    def __hash__(self):
        nodes = [n.id for n in self.nodes]
        nodes.sort()
        nodes = tuple(nodes)
        return hash(nodes)

    def does_contain(self, node):
        return node in self.nodes

    def should_contain(self, node):
        return all([n.connected(node) for n in self.nodes]) 

def main():
    sys.stderr.write("Starting\n")
    graph = load_sorted_adjacency_list()
    sys.stderr.write("Loaded "  + str(len(graph)) + " nodes\n")
    cliques = set()
    iterations = 0
    for node in graph:
        if iterations % 100 == 0:
            sys.stderr.write("Iteration " + str(iterations) + "\n")
        belongs = False
        for c in cliques:
            if c.should_contain(node):
                belongs = True
                c.nodes.add(node)
        if not belongs:
            new = Clique()
            new.nodes.add(node)
            for secondlook in node.neighbors:
                if new.should_contain(secondlook):
                    new.nodes.add(secondlook)
            cliques.add(new)
        iterations +=1
    sys.stderr.write("Computed cliques\n")
    clique_number = 0
    total_size = 0
    for c in cliques:
        size = len(c.nodes)
        total_size += size 
        for node in c.nodes:
            print json.dumps([clique_number, node.id])
        clique_number += 1
    avg_size = float(total_size) / float(len(cliques))
    sys.stderr.write("Number of cliques: " + str(len(cliques)) + "\n")
    sys.stderr.write("Average clique size: " + str(avg_size) + "\n")


def load_sorted_adjacency_list():
    nodes = {}
    with open(EDGES_FILE) as edges:
        for line in edges.readlines():
            edge = json.loads(line)
            ni = edge[0]
            nj = edge[1]
            if ni not in nodes:
                nodes[ni] = Node(ni)
            if nj not in nodes:
                nodes[nj] = Node(nj)
            nodes[ni].neighbors.add(nodes[nj])
            nodes[nj].neighbors.add(nodes[ni])
    return nodes.values()

#def very_slow_way_of_computing_cliques():
#    args = load_sql_data()
#    all_cliques = {}
#    for arg in args:
#        print "looking up subgraph for: ", arg
#        subgraph = lookup_neighbor_subgraph(arg)
#        cliques = find_cliques(subgraph)
#        for c in cliques:
#            all_cliques[c] = 1
#    print_cliques()
#
#def load_sql_data():
#    first = True
#    args = []
#    with open(CSV_FILENAME) as csv:
#        for line in csv.readlines():
#            if first:
#                first = False
#                continue
#            if len(args) > 2:
#                break
#            args.append(str(line))
#    return args
#
#def lookup_neighbor_subgraph(arg): 
#    
#    db = connect_db()
#    
#    # get all the queries that have this arg
#    arg = '42'
#    arg = arg.strip().replace('"','\"')
#    cursor = db.execute("SELECT query_id FROM args WHERE arg=?", [arg])
#    query_ids = [t[0] for t in cursor.fetchall()]
#    print query_ids
#    
#    # get all the args in those queries 
#    args = {}
#    for q in query_ids:
#        cursor = db.execute("SELECT arg FROM args WHERE query_id=?", [q])
#        for arg in [t[0] for t in cursor.fetchall()]:
#            args[arg] = 1
#    args = args.keys()
#    print args
#
#    n = len(args)
#    subgraph = np.zeros((n,n))
#    
#    # for each arg pair, figure out if they're connected 
#    for i in range(n):
#        for j in range(n):
#            cursor = db.execute("SELECT query_id FROM args WHERE arg=?", [arg[i]])
#            qi = set([t[0] for t in cursor.fetchall()])
#            cursor = db.execute("SELECT query_id FROM args WHERE arg=?", [arg[j]])
#            qj = set([t[0] for t in cursor.fetchall()])
#            print 'hi'
#            
#            #cursor = db.execute("SELECT * FROM args a, args b \
#            #                        WHERE a.arg=? \
#            #                            AND b.arg=? \
#            #                            AND a.query_id = b.query_id", 
#            #                            [args[i], args[j]])
#            if qi & qj: # set intersection
#                subgraph[i][j] = 1
#    print subgraph            
#    db.close()
#    return subgraph
#
#def find_cliques(subgraph):
#    print subgraph.shape 
#    return []
#
#def print_cliques():
#    pass

main()
