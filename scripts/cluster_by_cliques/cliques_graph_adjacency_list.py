#!/usr/bin/env python

import json
import sys

from itertools import chain

CLIQUE_FILE = "/data/deploy/boss/data/cliques.json"
EDGES_FILE = "/data/deploy/boss/data/args_adjacency_list_all.txt"

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
    return nodes

def read_in_cliques(nodes):
    cliques = {}
    with open(CLIQUE_FILE) as cliquesfile:
        for line in cliquesfile.readlines():
            item = json.loads(line)
            id = int(item[0])
            arg = item[1]
            node = nodes[arg]
            if not id in cliques:
                cliques[id] = Clique()
                cliques[id].id = id
            cliques[id].nodes.add(node)
    #for c in cliques.values():
    #    print len(c.nodes), c.id
    #exit()
    return filter(lambda x: len(x.nodes) > 2, cliques.values())

def share_an_edge(these, those):
    for ni in these:
        for nj in those:
            if ni.connected(nj): return True
    return False

def share_enough_edges(these, those):
    count = 0
    for ni in these:
        for nj in those:
            count += ni.connected(nj)
    n = float(len(these) + len(those))
    max_edges = (n*(n - 1.))/2.
    #print float(count) / max_edges
    return count > max_edges * .485 # empirically determined

def cliques_to_graph(cliques):
    nodes = {} 
    iterations = 0
    for i in range(len(cliques)):
        for j in range(i):
            if i == j: continue
            iterations += 1
            if iterations % 100000 == 0:
                sys.stderr.write("Cliques-to-graph iteration " + str(iterations) + "\n")
            #if iterations > 10000000: exit()
            ci = cliques[i]
            cj = cliques[j]
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
            if nodes[ci_nodes] == nodes[cj_nodes]: continue
            if share_enough_edges(ci.nodes, cj.nodes):
                print json.dumps((i, j))
                #nodes[ci_nodes].neighbors.add(nodes[cj_nodes])
                #nodes[cj_nodes].neighbors.add(nodes[ci_nodes])
    return nodes.values()

def main():
    sys.stderr.write("Starting\n")
    nodes = read_in_nodes()
    sys.stderr.write("Loaded "  + str(len(nodes)) + " nodes\n")
    old_cliques = read_in_cliques(nodes)
    sys.stderr.write("Finished reading in cliques\n")
    graph = cliques_to_graph(old_cliques)
    sys.stderr.write("Finished creating edges\n")

main()
