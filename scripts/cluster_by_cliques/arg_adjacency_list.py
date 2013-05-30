#!/usr/bin/env python

import json

from queryexplorer import connect_db

EDGES_FILE = "/Users/salspaugh/queryexplorer/data.storm/cluster_args_by_cliques/arg_adjacency_list_redundant.json"

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
            args = json.loads(line)
            args.sort()
            args = tuple(args)
            edges[args] = 1
    return set(edges)

def load_and_print_redundant_edges():
    db = connect_db()
    cursor = db.execute("SELECT arg, query_id FROM args")
    curr = prev = ""
    query_set = set()
    for (arg, query_id) in cursor.fetchall():
        curr = query_id
        if not curr == prev:
            print_edges(list(query_set))
            query_set.clear()
        query_set.add(arg)
        prev = curr
    db.close()

def print_edges(args):
    n = len(args)
    for i in range(n):
        for j in range(i):
            print json.dumps((args[i], args[j]))

main()
