#!/usr/bin/env python

import json
import sys

from itertools import chain
from queryexplorer import connect_db

def main():
    db = connect_db()
    args_cursor = db.execute("SELECT command_id, arg FROM args ORDER BY arg")
    args = {}
    done = 0
    for (command_id, arg) in args_cursor.fetchall():
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
    cmds = list(set(chain.from_iterable([v.keys() for v in args.values()])))
    cmds_idxs = zip(cmds, range(len(cmds)))
    for (cmd, idx) in cmds_idxs:
        print json.dumps((cmd, idx))

main()
