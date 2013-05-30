#!/usr/bin/env python

import numpy as np


CSV_FILENAME = '/Users/salspaugh/queryexplorer/data/queries_per_arg.csv'

ROWS = 41713 # number of unique args
COLS = 1020580 # number of queries

NUM_ARGS = 41713. # number of unique args
NUM_QUERIES = 1020580. # number of queries

def main():
    # X_ij = 1 if arg i is in query j
    # mu_i = E[Xi] = sum X_ij / NUM_QUERIES
    # sigma_i = (1 / NUM_QUERIES) (sum (X_ij - mu_i)**2) 
    mus = load_sql_data()
    sigmas = compute_variances(mus)
    covariances = compute_covariances(sigmas, mus)

def load_sql_data():
    first = True
    mus = {}
    with open(CSV_FILENAME) as csv:
        for line in csv.readlines():
            if first:
                first = False
                continue
            parts = line.split(',')
            mean = float(parts[0]) / NUM_QUERIES
            arg = ','.join(parts[1:])
            mus[arg] = mean
    return means

def compute_variances(mus):
    sigmas = {}
    for (arg, mean) in mus.iteritems(): 
        ones = 0.
        zeros = 0.
        sigmas[arg]  

def compute_covariances():
    pass

# Won't work -- too big of a matrix
def load_sql_data():
    data = np.zeros((ROWS, COLS))
    print "Initialized data matrix."
    first = True
    curr = prev = ""
    ridx = 0
    with open(CSV_FILENAME) as csv:
        for line in csv.readlines():
            if first:
                first = False
                continue
            parts = line.split(',')
            cidx = int(parts[0])
            curr = ','.join(parts[1:])
            if prev == curr:
                data[ridx][cidx] = 1.
            else:
                ridx += 1
            prev = curr
    return data

main()
