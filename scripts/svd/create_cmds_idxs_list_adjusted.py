#!/usr/bin/env python

import json
import re
import sys

from itertools import chain
from queryexplorer import connect_db

CUTME = "/Users/salspaugh/queryexplorer/data/svd/arg_count_greater_than_7"

def read_in_args_to_cut():
    cutme = []
    with open(CUTME) as cutfile:
        for line in cutfile.readlines():
            cutme.append(line.strip())
    return cutme

def main():
    cut = read_in_args_to_cut()
    db = connect_db()
    args_cursor = db.execute("SELECT command_id, arg FROM args ORDER BY arg")
    args = {}
    done = 0
    for (command_id, arg) in args_cursor.fetchall():
        arg = arg.strip()
        done = progress(done)
        if arg == '"':
            continue
        if arg in cut:
            continue
        new_arg = transform_arg(arg)
        if new_arg != arg:
            continue
        cmds_cursor = db.execute("SELECT command FROM commands WHERE id=?", [command_id])
        cmd = cmds_cursor.fetchall()[0][0]
        cmd = transform_cmd(cmd)
        if cmd == "search":
            continue
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

epochtimes = r"134[\d]{0,6}[*]|134[\d]{7}"
phonenumber = r"[\d]{10}"
datetime = r"[\d]{2}/[\d]{2}/[\d]{4}:[\d]{2}:[\d]{2}:[\d]{2}"
#integer = r"\d+"
usecasestr = r'"useCase=Lag, scriptRun=.*, lagScript=5MinLag"'
#trojanstr = r"Troj/[a-zA-Z0-9-]{5,14}"
cmdstr1 = r'.* \| sistats count by .* \| summaryindex .*'
cmdstr2 = r'.* transaction .* \| sitop .* \| summaryindex .*'
#ipaddr = r'[0-9\.\*]+'

def transform_arg(arg):
    if re.match(epochtimes, arg):
        return "salspaugh: UNIX epochs"
    if re.match(phonenumber, arg):
        return "salspaugh: phone number"
    if re.match(datetime, arg):
        return "salspaugh: datetime"
    if re.match(usecasestr, arg):
        return "salspaugh: use case string"
    if re.match(cmdstr1, arg):
        return "salspaugh: cmdstr1"
    if re.match(cmdstr2, arg):
        return "salspaugh: cmdstr2"
    return arg

def lookup_category(command):
    parts = command.split('(')
    main_command = parts[0].lower()
    category = "!!!"
    if main_command == "addtotals": # special case because parameter changes category
        if command.find('COL') > -1:
            category = cmd_lookup["addtotals col"]
        else:
            category = cmd_lookup["addtotals row"]
    else:
        try:
            category = cmd_lookup[main_command]
        except:
            print "Missing category for command: ", parts[0]
    return category

def transform_cmd(command):
    parts = command.split('(')
    main_command = parts[0].lower()
    if main_command == "addtotals": # special case because parameter changes category
        if command.find('COL') > -1:
            return "addtotals col"
        else:
            return "addtotals row"
    if main_command == "stats" or main_command == "eval":
        return command.lower()
    else:
        return main_command

def progress(done):
    done += 1
    if done % 100 == 0:
        sys.stderr.write(str(done) + " done\n")
        sys.stderr.flush()
    return done

main()
