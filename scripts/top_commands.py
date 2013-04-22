#!/usr/bin/env python

import json
import queryutils
import sys

from collections import defaultdict
from queryexplorer import connect_db

BYTES_IN_MB = 1048576

def main():
    done = 0
    commands_plus_counts = defaultdict(int)
    last_query = ""
    db = connect_db()
    select_cursor = db.execute("SELECT template FROM templates where template not null")
    for (template) in select_cursor.fetchall():
        done += 1
        if done % 100 == 0:
            sys.stderr.write(str(done) + " done\n")
            sys.stderr.flush()
        d = json.loads(template) # convert to parse tree node here
        t = ParseTreeNode.from_dict(d)
        commands_plus = t.get_commands_plus_list()
        for c in commands_plus:
            commands_plus_counts[c] += 1
    
    top_commands_plus = sorted(commands_plus.items(), key=lambda x: x[1], reverse=True)[:20]
    for (commands_plus, counts) in top_commands_plus:
        print counts, commands_plus

    db.close()

main()
