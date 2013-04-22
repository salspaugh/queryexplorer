#!/usr/bin/env python

import json

import numpy as np

NUM_ARGS = 59101 # cols
NUM_CMDS = 1722  # rows

ARGS_CMDS_CNTS_LIST = "/data/deploy/boss/arg_cmd_cnts.json"
CMDS_IDXS_LIST = "/data/deploy/boss/cmds_idx_list.json"

def main():
    z = np.zeros((NUM_CMDS, NUM_ARGS))
    args_cmds = read_args_cmds()
    cmds_idxs = read_cmds_idxs()
    col_idx = 0
    for (arg, cmds) in args_cmds:
        for (cmd, cnt) in cmds:
            row_idx = cmds_idxs[cmd]
            z[row_idx][col_idx] = int(cnt)
        col_idx += 1
    np.savetxt('args_cmds_frequency.csv', z, delimiter=',', fmt='%d')

def read_args_cmds():
    args_cmds = []
    with open(ARGS_CMDS_CNTS_LIST) as datafile:
        for line in datafile.readlines():
            args_cmds.append(json.loads(line))
    return args_cmds   

def read_cmds_idxs():
    cmds = {}
    with open(CMDS_IDXS_LIST) as datafile:
        for line in datafile.readlines():
            (cmd, idx) = json.loads(line)
            cmds[cmd] = idx
    return cmds

main()
