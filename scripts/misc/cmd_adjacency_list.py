#!/usr/bin/env python

import json

from queryexplorer import connect_db

EDGES_FILE = "/Users/salspaugh/queryexplorer/data/cmd_clustering/cmds_adjacency_list_redundant.txt"

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
            cmds = json.loads(line)
            cmds.sort()
            cmds = tuple(cmds)
            edges[cmds] = 1
    return set(edges)

def load_and_print_redundant_edges():
    db = connect_db()
    cursor = db.execute("SELECT command, query_id FROM commands")
    curr = prev = ""
    query_set = set()
    for (cmd, query_id) in cursor.fetchall():
        curr = query_id
        if not curr == prev:
            print_edges(list(query_set))
            query_set.clear()
        query_set.add(cmd)
        prev = curr
    db.close()

def print_edges(cmds):
    n = len(cmds)
    for i in range(n):
        for j in range(i):
            print json.dumps((cmds[i], cmds[j]))

main()
