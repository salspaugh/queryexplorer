#!/usr/bin/env python

import json

from queryexplorer import connect_db

EDGES_FILE = "/Users/salspaugh/queryexplorer/data/args_adjacency_list_redundant.txt"

def main():
    #load_and_print_redundant_edges()
    print_non_redundant_edges()

def print_non_redundant_edges():
    edges = list(uniquify_edges())
    edges.sort()
    for edge in edges: 
        print json.dumps(edge)

def uniquify_edges():
    edges = {}
    with open(EDGES_FILE) as datafile:
        for line in datafile.readlines():
            args = line.strip().split(',')
            args.sort()
            args = tuple(args)
            edges[args] = 1
    return set(edges)

def load_and_print_redundant_edges():
    db = connect_db()
    cursor = db.execute("SELECT arg, query_id FROM args")
    curr = prev = ""
    query_set = []
    for (arg, query_id) in cursor.fetchall():
        curr = query_id
        if not curr == prev:
            print_edges(query_set)
            del query_set[0:len(query_set)]
        query_set.append(arg)
        prev = curr
    db.close()

def print_edges(args):
    n = len(args)
    for i in range(n):
        for j in range(i):
            print ','.join([str(args[i]), str(args[j])])

main()
