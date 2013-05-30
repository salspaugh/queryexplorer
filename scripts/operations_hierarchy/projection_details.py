
from collections import defaultdict
from queryexplorer import connect_db

def main():
    db = connect_db()
    cursor = db.execute("SELECT command, text FROM commands, queries \
                            WHERE commands.query_id = queries.id \
                            AND operation_type=?", ["ExtendedProjection"])
    types = defaultdict(int)
    total = 0
    for (command, query) in cursor.fetchall():
        if command == "EVAL" or command == "EVAL(EQ)":
            continue
        total += 1
        added_to_something = False
        if command.find("REX") == 0:
            types["string extraction"] += 1
            added_to_something = True
        if command.find("EVAL") == 0:
            if command.find("CASE") > -1:
                types["conditional"] += 1
                added_to_something = True
            if command.find("COALESCE") > -1:
                types["conditional"] += 1
                added_to_something = True
            if command.find("CONCAT") > -1:
                types["string manipulation"] += 1
                added_to_something = True
            if command.find("DIVIDES") > -1:
                types["arithmetic"] += 1
                added_to_something = True
            if command.find("FLOOR") > -1:
                types["arithmetic"] += 1
                added_to_something = True
            if command.find("IF") > -1:
                types["conditional"] += 1
                added_to_something = True
            if command.find("LIKE") > -1:
                types["string match"] += 1
                added_to_something = True
            if command.find("MATCH") > -1:
                types["string match"] += 1
                added_to_something = True
            if command.find("MINUS") > -1:
                types["arithmetic"] += 1
                added_to_something = True
            if command.find("MVCOUNT") > -1:
                types["multivalue"] += 1
                added_to_something = True
            if command.find("MVINDEX") > -1:
                types["multivalue"] += 1
                added_to_something = True
            if command.find("PLUS") > -1:
                types["arithmetic"] += 1
                added_to_something = True
            if command.find("REPLACE") > -1:
                types["string concatenation"] += 1
                added_to_something = True
            if command.find("ROUND") > -1:
                types["arithmetic"] += 1
                added_to_something = True
            if command.find("SPLIT") > -1:
                types["string concatenation"] += 1
                added_to_something = True
            if command.find("STRPTIME") > -1:
                types["time manipulation"] += 1
                added_to_something = True
            if command.find("SUBSTR") > -1:
                types["string manipulation"] += 1
                added_to_something = True
            if command.find("TIMES") > -1:
                types["arithmetic"] += 1
                added_to_something = True
            if command.find("TONUMBER") > -1:
                types["conversion"] += 1
                added_to_something = True
            if command.find("TRIM") > -1:
                types["string manipulation"] += 1
                added_to_something = True
            if command.find("UPPER") > -1:
                types["string manipulation"] += 1
                added_to_something = True

        if not added_to_something:
            print "Missed a case!", command


    cursor = db.execute("SELECT command, text FROM commands, queries \
                            WHERE commands.query_id = queries.id \
                            AND operation_type=?", ["Projection"])
    for (command, query) in cursor.fetchall():
        total += 1
        added_to_something = False
        if command.find("MINUS") > -1:
            types["unproject"] += 1
            added_to_something = True
        else:
            types["project"] += 1
            added_to_something = True

        if not added_to_something:
            print "Missed a case!", command


    cursor = db.execute("SELECT command, text FROM commands, queries \
                            WHERE commands.query_id = queries.id \
                            AND operation_type=?", ["TransformingProjection"])
    for (command, query) in cursor.fetchall():
        total += 1
        added_to_something = False
        if command.find("BUCKET") == 0:
            types["bucket"] += 1
            added_to_something = True
        if command.find("CONVERT") == 0:
            types["conversion"] += 1
            added_to_something = True
        if command.find("FILLNULL") == 0:
            types["fill null"] += 1
            added_to_something = True
        if command.find("MAKEMV") == 0:
            types["multivalue"] += 1
            added_to_something = True
        if command.find("MULTIKV") == 0:
            types["string extraction"] += 1
            added_to_something = True
        if command.find("REPLACE") == 0:
            types["string manipulation"] += 1
            added_to_something = True

        if not added_to_something:
            print "Missed a case!", command

    db.close()    
    print_results(types, total)

def print_results(types, total):
    for (type, count) in (sorted(types.iteritems(), key=lambda x:x[1])):
        print type, ":", (float(count) / float(total)) * 100

main()
