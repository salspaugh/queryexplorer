#!/usr/bin/env python

import json

ARG_CLIQUES = "/deploy/data/boss/data/cliques.json"
CLIQUE_CLIQUES = "/deploy/data/boss/data/cliques_of_cliques.json"

def read_in_arg_cliques():
    arg_cliques = {}
    with open(ARG_CLIQUES) as argcliquesfile:
        for line in argcliquesfile.readlines():
            entry = json.loads(line)
            id = int(entry[0])
            arg = entry[1]
            arg_cliques[id] = arg
    return arg_cliques

def read_in_clique_cliques():
    clique_cliques = {}
    with open(CLIQUE_CLIQUES) as cliquecliquesfile:
        for line in cliquecliquesfile.readlines():
            entry = json.loads(line)
            id = int(entry[0])
            clique = entry[1]
            clique_cliques[id] = clique
    return clique_cliques

def main():
    arg_cliques = read_in_arg_cliques()
    clique_cliques = read_in_clique_cliques()
    aggregated_arg_cliques = {}
    for (cid, arg_clique_ids) in clique_cliques.iteritems():
        if not cid in aggregated_arg_cliques:
            aggregated_arg_cliques[cid] = set()
        for arg_clique_id in arg_clique_ids:
            aggregated_arg_cliques[cid].update(arg_cliques[arg_clique_id])
    aggregated_arg_cliques = sorted(lambda x: len(x[1]), aggregated_arg_cliques.iteritems(), reverse=True) 
    for (cid, args) in aggregated_arg_cliques:
        for arg in args:
            json.dumps((cid, arg))

main()
