#!/usr/bin/env python

import json
import sys

from queryexplorer import connect_db

CUTME = "/Users/salspaugh/queryexplorer/data/svd/arg_count_greater_than_7"

def read_in_args_to_cut():
    cutme = []
    with open(CUTME) as cutfile:
        for line in cutfile.readlines():
            cutme.append(line.strip())
    return cutme

def main():
    cutme = read_in_args_to_cut()
    db = connect_db()
    args_cursor = db.execute("SELECT command_id, arg FROM args ORDER BY arg")
    args = {}
    done = 0
    for (command_id, arg) in args_cursor.fetchall():
        if arg in cutme: continue
        done += 1
        if done % 100 == 0:
            sys.stderr.write(str(done) + " done\n")
            sys.stderr.flush()
        if arg == '"':
            continue
        cmds_cursor = db.execute("SELECT command FROM commands WHERE id=?", [command_id])
        cmd = cmds_cursor.fetchall()[0][0]
        if not arg in args:
            args[arg] = {}
        if not cmd in args[arg]:
            args[arg][cmd] = 0
        args[arg][cmd] += 1
    db.commit()
    for (arg, cmd_counts) in args.iteritems():
        print json.dumps([arg, cmd_counts.items()])
    db.close()

main()
