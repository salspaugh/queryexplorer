#!/usr/bin/env python

import json
import sys

from itertools import chain

CLIQUE_FILE = "/data/deploy/boss/data/cliques.json"
EDGES_FILE = "/data/deploy/boss/data/args_adjacency_list_all.txt"
#CLIQUE_EDGES_FILE = "/data/deploy/boss/data/cliques_graph_adjacency_list.json"
CLIQUE_EDGES_FILE = "/data/deploy/boss/data/shorter_cliques_graph_adjacency_list.json"

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

    def neighborfy_nodes(self):
        for node in self.nodes:
            node.neighbors |= (self.nodes - set([node]))

def read_in_nodes():
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
    nodes = nodes.values()
    nodes_dict = dict(zip([n.id for n in nodes], nodes))
    return nodes_dict

def read_in_cliques(nodes):
    cliques = {}
    #first = True
    with open(CLIQUE_FILE) as cliquesfile:
        for line in cliquesfile.readlines():
            item = json.loads(line)
            id = int(item[0])
            arg = item[1]
            node = nodes[arg]
            if not id in cliques:
                #if not first:
                #    cliques[id-1].neighborfy_nodes()
                #first = False
                cliques[id] = Clique()
            cliques[id].nodes.add(node)
    #cliques[id].neighborfy_nodes()
    return filter(lambda x: len(x.nodes) > 2, cliques.values())

def share_an_edge(these, those):
    for ni in these:
        for nj in those:
            if ni.connected(nj): return True
    return False

def cliques_to_graph(cliques):
    nodes = {} 
    iterations = 0
    for i in range(len(cliques)):
        for j in range(i):
            ci = cliques[i]
            cj = cliques[j]
            iterations += 1
            if iterations % 10000 == 0:
                sys.stderr.write("Cliques-to-graph iteration " + str(iterations) + "\n")
            ci_nodes = list([n.id for n in ci.nodes])
            ci_nodes.sort()
            ci_nodes = tuple(ci_nodes)
            if ci_nodes not in nodes:
                nodes[ci_nodes] = Node(ci_nodes)
            cj_nodes = list([n.id for n in cj.nodes])
            cj_nodes.sort()
            cj_nodes = tuple(cj_nodes)
            if cj_nodes not in nodes:
                nodes[cj_nodes] = Node(cj_nodes)
            if nodes[ci_nodes] == nodes[cj_nodes]:
                continue
            #print "cinodes", ci.nodes
            #print "cjnodes", cj.nodes
            if share_an_edge(ci.nodes, cj.nodes):
                nodes[ci_nodes].neighbors.add(nodes[cj_nodes])
                nodes[cj_nodes].neighbors.add(nodes[ci_nodes])
    return nodes.values()

def read_in_cliques():
    nodes = {}
    iterations = 0
    with open(CLIQUE_EDGES_FILE) as edges:
        for line in edges.readlines():
            iterations += 1
            if iterations % 100 == 0:
                sys.stderr.write("Cliques-to-graph iteration " + str(iterations) + "\n")
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
    #nodes_dict = dict(zip([n.id for n in nodes], nodes))
    #return nodes_dict

def main():
    sys.stderr.write("Starting\n")
    #nodes = read_in_nodes()
    #sys.stderr.write("Loaded "  + str(len(nodes)) + " nodes\n")
    #old_cliques = read_in_cliques(nodes)
    ##for c in old_cliques:
    ##    print c.nodes
    #graph = cliques_to_graph(old_cliques)
    
    graph = read_in_cliques()
    sys.stderr.write("Loaded "  + str(len(graph)) + " clique nodes\n")
    
    iterations = 0
    cliques = set()
    for node in graph:
        if iterations % 100 == 0:
            sys.stderr.write("Cliques-of-cliques iteration " + str(iterations) + "\n")
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
        #print c
        size = len(c.nodes)
        total_size += size 
        nodes = [n.id for n in c.nodes]
        #nodes = set(chain.from_iterable(nodes))
        for node in nodes:
            print json.dumps([clique_number, node])
        clique_number += 1
    avg_size = float(total_size) / float(len(cliques))
    sys.stderr.write("Number of cliques: " + str(len(cliques)) + "\n")
    sys.stderr.write("Average clique size: " + str(avg_size) + "\n")

main()
