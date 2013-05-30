
from collections import defaultdict
from queryexplorer import connect_db

import queryutils
import sys

def main():
    db = connect_db()
    done = 0
    select_cursor = db.execute("SELECT min(id), text FROM queries WHERE id>? GROUP BY text", [0])
    schemas = {}
    for (id, query) in select_cursor.fetchall():
        done += 1
        if done % 10 == 0:
            sys.stderr.write(str(done) + " done\n")
            sys.stderr.flush()
        schema = queryutils.extract_schema(query) 
        if not schema is None:
            schemas[id] = (text, schema)
            print "query:", id
            print "schema:"
            print schema
            print
    
    users_by_query_text = {}
    for (id, (text, schema)) for schemas.iteritems():
        users_by_query_text[text] = set()
        select_cursor = db.execute("SELECT user_id FROM queries WHERE text=?", [text])
        for user_id in select_cursor.fetchall():
            users_by_query_text[text].add(user_id)
    
    first = schemas_to_merge.pop()
    first_id = first[0]
    holdout_text = first[1]
    holdout_schema = first[2]
    holdout_id = -1
    while holdout_id != first_id: 
        merged = False
        for (id, text, schema) in schemas_to_merge:
            holdout_users = users_by_query_text[holdout_text]
            users = users_by_query_text[text]
            if len(holdout_users & users) > 0 and schema.mergeable(holdout_schema):
                schema.merge_schema(holdout_schema)
                merged = True
                break
        if not merged:
            if holdout_id = -1:
                holdout_id = first_id
            schemas_to_merge.append((holdoutid, holdout_text, holdout_schema))
        next = schemas_to_merge.pop()
        holdout_id = next[0]
        holdout_text = next[1]
        holdout_schema = next[2]

        #check_cursor = db.execute("SELECT * FROM schemas \
        #                            WHERE query_id=?", [str(id)])
        #if len(check_cursor.fetchall()) == 0:
        #    schema = queryutils.extract_schema(query) 
        #    if schema is None:
        #        last_query = query
        #        last_failed = True
        #        continue
        #    s = schema.dumps()
        #    insert_cursor.execute("INSERT INTO schemas (query_id, schema) \
        #                    VALUES (?,?)", [id, s])
        #    db.commit() 
    db.close()

main()
