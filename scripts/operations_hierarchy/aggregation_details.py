
from collections import defaultdict
from queryexplorer import connect_db

def main():
    db = connect_db()
    cursor = db.execute("SELECT command, text FROM commands, queries \
                            WHERE commands.query_id = queries.id \
                            AND operation_type=?", ["Aggregation"])
    types = defaultdict(int)
    total = 0
    for (command, query) in cursor.fetchall():
        total += 1
        added_to_something = False
        if command.find("TOP") == 0:
            types["top"] += 1
            added_to_something += 1
        if command.find("TIMECHART") == 0:
            types["visualize over time"] += 1
            added_to_something = True
        if command.find("CHART") == 0 or command.find("TIMECHART") == 0 or command.find("SPARKLINE") > -1:
            types["visualization"] += 1
            added_to_something = True
        if command.find("COUNT") > -1 or command.find("C") > -1:
            types["count"] += 1
            added_to_something = True
        if command.find("DISTINCT_COUNT") > -1 or command.find("DC") > -1:
            types["distinct count"] += 1
            added_to_something = True
        if command.find("AVG") > -1 or command.find("MEDIAN") > -1 or command.find("MODE") > -1:
            types["average, median, mode"] += 1
            added_to_something = True
        if command.find("VAR") > -1:
            types["other"] += 1
            added_to_something = True
        if command.find("MAX") > -1:
            types["max"] += 1
            added_to_something = True
        if command.find("MIN") > -1:
            types["min"] += 1
            added_to_something = True
        if command.find("LAST") > -1:
            types["other"] += 1
            added_to_something = True
        if command.find("VALUES") > -1:
            types["other"] += 1
            added_to_something = True
        if command.find("RANGE") > -1:
            types["other"] += 1
            added_to_something = True
        if command.find("SUM") > -1:
            types["sum"] += 1
            added_to_something = True
        if command.find("LIST") > -1:
            types["other"] += 1
            added_to_something = True
        if command.find("PER_MINUTE") > -1:
            types["other"] += 1
            added_to_something = True
        if command.find("PER_HOUR") > -1:
            types["other"] += 1
            added_to_something = True
        if command.find("P9") > -1 or command.find("PERC") > -1:
            types["other"] += 1
            added_to_something = True
        if command.find("EVAL") > -1:
            types["arithmetic or boolean"] += 1
            added_to_something = True
        if command.find("BY") > -1:
            types["grouped"] += 1
            added_to_something = True
        if command.find("AS") > -1:
            types["renamed"] += 1
            added_to_something = True

        if not added_to_something:
            print "Missed a case!", command
    db.close()    
    print_results(types, total)

def print_results(types, total):
    for (type, count) in (sorted(types.iteritems(), key=lambda x:x[1])):
        print type, ":", (float(count) / float(total)) * 100

main()
