#!/usr/bin/env python

import json
import sys

from queryexplorer import connect_db

def main():
    db = connect_db()
    args_cursor = db.execute("select command_id, arg from (select command_id, arg from commands, args, templates, queries where queries.id = commands.query_id and queries.id = args.query_id and templates.query_id = queries.id group by arg, command, template) order by arg")
    args = {}
    done = 0
    for (command_id, arg) in args_cursor.fetchall():
        done += 1
        if done % 100 == 0:
            sys.stderr.write(str(done) + " done\n")
            sys.stderr.flush()
        if arg == '"':
            continue
        arg = transform_argument(arg)
        cmds_cursor = db.execute("SELECT command FROM commands WHERE id=?", [command_id])
        cmd = cmds_cursor.fetchall()[0][0]
        cmd = transform_command(cmd)
        if not arg in args:
            args[arg] = {}
        if not cmd in args[arg]:
            args[arg][cmd] = 0
        args[arg][cmd] += 1
    for (arg, cmd_counts) in args.iteritems():
        print json.dumps([arg, cmd_counts.items()])
    db.close()

def transform_command(cmd):
    cmd = cmd.strip()
    if cmd.find("SEARCH") == 0:
        return "search"
    if cmd.find("REX") == 0:
        return "rex"
    if cmd.find("MAKEMV") == 0:
        return "makemv"
    if cmd.find("MULTIKV") == 0:
        return "multikv"
    if cmd.find("COLLECT") == 0:
        return "collect"

    # removing options
    cmd = cmd.replace("EQ(SPAN),", "")
    cmd = cmd.replace(",EQ(SPAN)", "")
    cmd = cmd.replace("EQ(SPAN)", "")
    cmd = cmd.replace("EQ(TIMEFORMAT),", "")
    cmd = cmd.replace(",EQ(USENULL)", "")
    cmd = cmd.replace(",EQ(USEOTHER)", "")
    cmd = cmd.replace("DISTINCT_COUNT", "DC")
    cmd = cmd.replace("COUNT", "C")
    cmd = cmd.replace("()", "")

    # remove redundant function calls
    if cmd.find("TIMECHART(SUM(AS)") == 0:
        return "timechart(sum(as))"
    if cmd == "TIMECHART(AVG,AVG(BY))":
        return "timechart(avg(by))"
    if cmd == "CHART(C,C)":
        return "chart(c)"
    if cmd.find("EVAL(EQ(IF(OR(EQ,EQ") == 0:
        return "eval(eq(if(or(eq))))"
    if cmd.find("TIMECHART(AVG(AS),AVG(AS)") == 0:
        return "timechart(avg(as))"
    if cmd.find("TIMECHART(AVG,AVG") == 0:
        return "timechart(avg)"
    if cmd == "TIMECHART(DC,DC)":
        return "timechart(dc)"
    if cmd == "TIMECHART(SUM,SUM)":
        return "timechart(sum)"
    return cmd.lower()

def transform_argument(arg):
    return arg.lower()

main()

