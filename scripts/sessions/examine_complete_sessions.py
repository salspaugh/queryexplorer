
import json
from collections import defaultdict
from queryexplorer import connect_db
from splparser.parsetree import ParseTreeNode

# same queries
# same parsetrees
# generalizing parsetrees
# specializing parsetrees
# other

def main():
    len_one_sessions = 0
    generalizing_parsetrees = 0
    specializing_parsetrees = 0
    identical_parsetrees = 0
    total = 0
    inds = []
    gens = []
    specs = []
    others = []
    sessions = read_in_sessions()
    for (session_id, queries) in sessions.iteritems():
        queries = sorted(queries, key=lambda x: x[0])
        if len(queries) == 1:
            len_one_sessions += 1
        elif is_identical_parsetrees(queries):
            identical_parsetrees += 1
            inds.append((session_id, queries))
        elif is_generalizing_parsetrees(queries):
            generalizing_parsetrees += 1
            gens.append((session_id, queries))
        elif is_specializing_parsetrees(queries):
            specializing_parsetrees += 1 
            specs.append((session_id, queries))
        else:
            others.append((session_id, queries))
        total += 1
    other = total - len_one_sessions - generalizing_parsetrees - specializing_parsetrees - identical_parsetrees
    print "Length one sessions: ", len_one_sessions
    print "Generalizing parsetrees sessions: ", generalizing_parsetrees
    print "Specializing parsetree sessions: ", specializing_parsetrees
    print "Identical parsetree sessions: ", identical_parsetrees
    print "Other (unknown): ", other
    print "Total: ", total
    print
    
    # Print inds info.
    inds_avg_time_length = 0.
    inds_min_time_length = 1e12
    inds_max_time_length = 0.
    inds_avg_item_length = 0.
    inds_min_item_length = 1e12
    inds_max_item_length = 0.
    for (sid, templates) in inds:
        first = True
        for (time, qid, template) in templates:
            if first:
                first = False
                firsttime = time
        time_length = time - firsttime
        item_length = len(templates)
        inds_max_time_length = max(time_length, inds_max_time_length)
        inds_min_time_length = min(time_length, inds_min_time_length)
        inds_avg_time_length += time_length
        inds_max_item_length = max(item_length, inds_max_item_length)
        inds_min_item_length = min(item_length, inds_min_item_length)
        inds_avg_item_length += item_length
    inds_avg_time_length = inds_avg_time_length / len(inds)
    inds_avg_item_length = inds_avg_item_length / len(inds)
    print "Identical sessions max time length:", inds_max_time_length
    print "Identical sessions min time length:", inds_min_time_length
    print "Identical sessions avg time length:", inds_avg_time_length
    print
    print "Identical sessions max item length:", inds_max_item_length
    print "Identical sessions min item length:", inds_min_item_length
    print "Identical sessions avg item length:", inds_avg_item_length
    print

    # Print gens info.
    gens_avg_time_length = 0.
    gens_min_time_length = 1e12
    gens_max_time_length = 0.
    gens_avg_item_length = 0.
    gens_min_item_length = 1e12
    gens_max_item_length = 0.
    for (sid, templates) in gens:
        first = True
        for (time, qid, template) in templates:
            if first:
                first = False
                firsttime = time
        time_length = time - firsttime
        item_length = len(templates)
        gens_max_time_length = max(time_length, gens_max_time_length)
        gens_min_time_length = min(time_length, gens_min_time_length)
        gens_avg_time_length += time_length
        gens_max_item_length = max(item_length, gens_max_item_length)
        gens_min_item_length = min(item_length, gens_min_item_length)
        gens_avg_item_length += item_length
    gens_avg_time_length = gens_avg_time_length / len(gens)
    gens_avg_item_length = gens_avg_item_length / len(gens)
    print "Generalizing sessions max time length:", gens_max_time_length
    print "Generalizing sessions min time length:", gens_min_time_length
    print "Generalizing sessions avg time length:", gens_avg_time_length
    print
    print "Generalizing sessions max item length:", gens_max_item_length
    print "Generalizing sessions min item length:", gens_min_item_length
    print "Generalizing sessions avg item length:", gens_avg_item_length
    print
                 
    # Print specs info.
    specs_avg_time_length = 0.
    specs_min_time_length = 1e12
    specs_max_time_length = 0.
    specs_avg_item_length = 0.
    specs_min_item_length = 1e12
    specs_max_item_length = 0.
    for (sid, templates) in specs:
        first = True
        for (time, qid, template) in templates:
            if first:
                first = False
                firsttime = time
        length = time - firsttime
        item_length = len(templates)
        specs_max_time_length = max(length, specs_max_time_length)
        specs_min_time_length = min(length, specs_min_time_length)
        specs_avg_time_length += specs_avg_time_length
        specs_max_item_length = max(item_length, specs_max_item_length)
        specs_min_item_length = min(item_length, specs_min_item_length)
        specs_avg_item_length += item_length
    specs_avg_time_length = length / len(specs)
    specs_avg_item_length = specs_avg_item_length / len(specs)
    print "Specializing sessions max time length:", specs_max_time_length
    print "Specializing sessions min time length:", specs_min_time_length
    print "Specializing sessions avg time length:", specs_avg_time_length
    print
    print "Specializing sessions max item length:", specs_max_item_length
    print "Specializing sessions min item length:", specs_min_item_length
    print "Specializing sessions avg item length:", specs_avg_item_length
    print
                 
    # Print others.
    db = connect_db()
    for (sid, templates) in others:
        print
        for (time, qid, template) in templates:
            qcursor = db.execute("SELECT text FROM queries WHERE id=?", [qid])
            query = qcursor.fetchall()[0][0]
            print query.strip()
            #template.print_tree()
            print
        print "__________________________________________________________________________"
    db.close()

def is_generalizing_parsetrees(queries):
    prev = curr = None
    first = True
    for (time, qid, template) in queries:
        prev = curr
        curr = template
        if first:
            first = False
            continue
        if not prev.is_supertree_of(curr):
            return False
    return True

def is_specializing_parsetrees(queries):
    prev = curr = None
    first = True
    for (time, qid, template) in queries:
        prev = curr
        curr = template
        if first:
            first = False
            continue
        if not curr.is_supertree_of(prev):
            return False
    return True

def is_identical_parsetrees(queries):
    prev = None
    curr = None
    first = True
    for (time, qid, template) in queries:
        curr = template
        if first:
            first = False
            prev = curr
            continue
        if not prev == curr:
            return False
        prev = curr
    return True

def print_all_sessions():
    sessions = read_in_sessions()
    for (session_id, queries) in sessions.iteritems():
        if len(queries) == 1: continue
        queries = sorted(queries, key=lambda x: x[0])
        for (time, query_id, template) in queries:
            template.print_tree()
            print
        print "__________________________________________________________________________"

def read_in_sessions():
    sessions = defaultdict(list)
    db = connect_db()
    select_cursor = db.execute("SELECT session_id, query_id, template FROM templated_sessions ORDER BY session_id")
    for (session_id, query_id, template) in select_cursor.fetchall():
        time_cursor = db.execute("SELECT time FROM queries WHERE id=?", [query_id])
        time = float(time_cursor.fetchall()[0][0])
        template = ParseTreeNode.from_dict(json.loads(template))
        sessions[session_id].append((time, query_id, template))
    db.close()
    return sessions


main()
