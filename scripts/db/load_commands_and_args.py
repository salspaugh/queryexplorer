#!/usr/bin/env python

import queryutils
import sys

from collections import defaultdict
from queryexplorer import connect_db

BYTES_IN_MB = 1048576

def main():
    done = 0
    db = connect_db()
    select_cursor = db.execute("SELECT min(id), text FROM queries WHERE id>? GROUP BY text", [0])
    for (id, query) in select_cursor.fetchall():
        done += 1
        if done % 100 == 0:
            sys.stderr.write(str(done) + " done\n")
            sys.stderr.flush()
        check_cursor = db.execute("SELECT * FROM commands \
                                    WHERE query_id=?", [str(id)])
        if len(check_cursor.fetchall()) == 0:
            parsetree = queryutils.parse_query(query)
            if parsetree is None:
                last_query = query
                last_failed = True
                continue
            commands_and_args = parsetree.command_arg_tuple_list()
            insert_commands_and_args(db, id, commands_and_args)
    db.close()

def insert_commands_and_args(db, qid, commands_and_args):
    for (cmd, args) in commands_and_args:
        cmd_cursor = db.cursor()
        cmd_cursor.execute("INSERT INTO commands (query_id, command) \
                        VALUES (?,?)", [qid, cmd])
        cid = cmd_cursor.lastrowid
        db.commit()
        for (arg, field) in args:
            field = 1 if field else 0
            arg_cursor = db.cursor()
            arg_cursor.execute("INSERT INTO args (query_id, command_id, arg, field) \
                                VALUES (?,?,?, ?)", [str(qid), str(cid), arg, field])
            db.commit()

main()
