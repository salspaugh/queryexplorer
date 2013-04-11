#!/usr/bin/env python

import queryutils
import sys

from collections import defaultdict
from queryexplorer import connect_db

BYTES_IN_MB = 1048576

def main():
    done = 0
    #seen = defaultdict(int)
    last_query = ""
    db = connect_db()
    select_cursor = db.execute("SELECT id, text FROM queries WHERE id>?", [177189])
    for (id, query) in select_cursor.fetchall():
        done += 1
        if done % 100 == 0:
            sys.stderr.write(str(done) + " done\n")
            sys.stderr.flush()
        if query == last_query and last_failed:
            last_query = query
            continue
        else:
            last_query = query
            last_failed = False
        check_cursor = db.execute("SELECT * FROM templates \
                                    WHERE query_id=?", [str(id)])
        if len(check_cursor.fetchall()) == 0:
            template = queryutils.extract_template(query) 
            if template is None:
                last_query = query
                last_failed = True
                continue
            s = template.dumps()
            insert_cursor = db.cursor()
            insert_cursor.execute("INSERT INTO templates (query_id, template) \
                            VALUES (?,?)", [id, s])
            db.commit()
            #seen[s] += 1 

    #print "Number of templates: ", len(seen.keys())
    #templates = sorted(seen.items(), key=lambda x: x[1], reverse=True)
    #for (template, count) in templates:
    #    print "Template: \n", template
    #    print "Count: ", count
    #    print
    db.close()

main()
