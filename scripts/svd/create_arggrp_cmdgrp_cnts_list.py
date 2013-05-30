#!/usr/bin/env python

import json
import sys

from queryexplorer import connect_db

def main():
    db = connect_db()
    args_cursor = db.execute("SELECT count(id) as cnt, clique_label, command_id FROM args GROUP BY clique_label, command_id")
    argrps = {}
    done = 0
    for (cnt, label, cmdid) in args_cursor.fetchall():
        done += 1
        if done % 100 == 0:
            sys.stderr.write(str(done) + " done\n")
            sys.stderr.flush()
        cmds_cursor = db.execute("SELECT category FROM commands WHERE id=?", [cmdid])
        category = cmds_cursor.fetchall()[0][0]
        if not label in argrps:
            argrps[label] = {}
        if not category in argrps[label]:
            argrps[label][category] = 0
        argrps[label][category] += 1
    db.commit()
    for (arglabel, cmdgrps) in argrps.iteritems():
        print json.dumps([arglabel, cmdgrps.items()])

main()
