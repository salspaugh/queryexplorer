
from collections import defaultdict
from queryexplorer import connect_db

import re

time_pattern = r".*(time|Time|TIME).*(<|<=|=|!=|>=|>)[.]*"

def main():
    db = connect_db()
    cursor = db.execute("SELECT command, text FROM commands, queries \
                            WHERE commands.query_id = queries.id \
                            AND operation_type=?", ["FilterSelection"])
    types = defaultdict(int)
    total = 0
    for (command, query) in cursor.fetchall():
        total += 1
        added_to_something = False
        if command.find("DEDUP") == 0:
            types["filter out duplicates"] += 1
            added_to_something = True
        if command.find("HEAD") == 0:
            types["filter on index"] += 1
            added_to_something = True
        if command.find("REGEX") == 0:
            c = command.lstrip("REGEX")
            types["filter on string match"] += 1
            added_to_something = True
        if command == "SEARCH" or command == "SEARCH(SOURCE)":
            types["filter on string match"] += 1
            added_to_something = True
        else:
            c = command.strip("SEARCH")
            c = c.strip("WHERE")
            s = get_filter_stage(query)
            if c.find("(AND") == 0 or c.find("(EQ") == 0:
                types["filter on multiple conditions"] += 1
                added_to_something = True
            if c.find("(OR") == 0:
                types["filter on multiple conditions"] += 1
                added_to_something = True
            if c.find("(NOT") == 0 or c.find("(NE") == 0:
                types["filter on multiple conditions"] += 1
                added_to_something = True
            if c.find("(GT") > -1 or c.find("GE") > -1 or c.find("(LT") > -1 or c.find("(LE") > -1:
                types["filter with numerical bound"] += 1
                added_to_something = True
            if c.find("(ISNULL") > -1 or c.find("(ISNOTNULL") > -1:
                types["filter on nullness"] += 1
                added_to_something = True
            if c.find("SOURCETYPE") > -1 or c.find("SOURCE") > -1 or c.find("HOST") > -1 or c.find("EVENTTYPE") > -1 or query.find("index") > -1:
                types["filter on source"] += 1
                added_to_something = True
            if c.find("EARLIEST") > -1 or c.find("LATEST") > -1:
                types["filter on time"] += 1
                added_to_something = True
            if re.match(time_pattern,s):
                types["filter on time"] += 1
                added_to_something = True
        if not added_to_something:
            print "Missed a case!", command
    db.close()    
    print_results(types, total)

def get_filter_stage(query):
    stages = query.split("|")
    for stage in stages:
        stage = stage.strip()
        parts = stage.split()
        if parts[0] == "search":
            return stage
        if parts[0] == "where":
            return stage

def print_results(types, total):
    for (type, count) in (sorted(types.iteritems(), key=lambda x:x[1])):
        print type, ":", (float(count) / float(total)) * 100

main()
