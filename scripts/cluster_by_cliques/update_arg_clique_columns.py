#!/usr/bin/env python

import json
import queryutils
import sys

from queryexplorer import connect_db

ARG_CLUSTERS = "/Users/salspaugh/queryexplorer/data/arg_clustering/new_arg_clusters.json"
CLUSTER_LABELS = "/Users/salspaugh/queryexplorer/data/arg_clustering/new_arg_groups.txt"

def main():
    db = connect_db()
    arg_clusters = read_in_arg_clusters()
    cluster_labels = read_in_cluster_labels()
    arg_labels = make_arg_labels(arg_clusters, cluster_labels)
    for (arg, labels) in arg_labels.iteritems():
        if len(labels) == 1:
            cluster_id = min(arg_clusters[arg])
            label = labels.pop()
            print "adding to", arg, "id", cluster_id, "label", label
            single_cursor = db.cursor()
            single_cursor.execute("UPDATE args SET clique_id=?, clique_label=? WHERE arg=?", [cluster_id, label, arg])
            db.commit()
        if len(labels) > 1:
            labels = ';'.join([str(label) for label in labels])
            print "adding to", arg, "id -1 label", labels
            multiple_cursor = db.cursor()
            multiple_cursor.execute("UPDATE args SET clique_id=?, clique_label=? WHERE arg=?", [-1, labels, arg])
            db.commit()
    db.close()

def make_arg_labels(arg_clusters, cluster_labels):
    arg_labels = {}
    for (arg, clusters) in arg_clusters.iteritems():
        if not arg in arg_labels:
            arg_labels[arg] = set()
        for cluster in clusters:
            try:
                label = cluster_labels[cluster]
            except:
                label = cluster
            arg_labels[arg].add(label)
    return arg_labels

def read_in_arg_clusters():
    arg_clusters = {}
    with open(ARG_CLUSTERS) as argclustersfile:
        for line in argclustersfile.readlines():
            (id, arg) = json.loads(line)
            if not arg in arg_clusters:
                arg_clusters[arg] = set()
            arg_clusters[arg].add(int(id))
    return arg_clusters

def read_in_cluster_labels():
    cluster_labels = {}
    with open(CLUSTER_LABELS) as clusterlabelsfile:
        for line in clusterlabelsfile.readlines():
            parts = line.strip().split(',')
            id = int(parts[0])
            label = ','.join(parts[1:]).strip()
            cluster_labels[id] = label
    return cluster_labels

main()
