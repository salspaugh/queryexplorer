
from collections import defaultdict
from queryexplorer import connect_db

def main():
    sessions = read_in_templatized_sessions()
    print "Number of complete sessions:", len(sessions)

def read_in_templatized_sessions():
    session_queries = defaultdict(list)
    session_templates = defaultdict(list)
    
    db = connect_db()
   
    cursor = db.execute("SELECT queries.session_id, templates.query_id, templates.template \
                            FROM queries, templates, users \
                            WHERE queries.id = templates.query_id \
                                AND users.id = queries.user_id \
                                AND users.user_type = ?", ["person"])
    num_queries = 0
    for (session_id, query_id, template) in cursor.fetchall():
        session_templates[session_id].append((query_id, template))
        num_queries += 1

    print "Formed session_templates dict with length", len(session_templates)
    print "\t and with number of queries", num_queries

    complete_sessions = {}
    for (session_id, query_templates) in session_templates.iteritems():
        cursor = db.execute("SELECT session_id, id FROM queries \
                                WHERE session_id = ?", [session_id])
        queries = []
        for (sid, qid) in cursor.fetchall():
            queries.append(qid)
        if len(queries) == len(query_templates):
            print "Have a complete session of length", len(query_templates)
            complete_sessions[session_id] = query_templates
            for (query_id, template) in query_templates:
                print "This is happening."
                insert_cursor = db.cursor()
                insert_cursor.execute("INSERT INTO templated_sessions \
                                        (session_id, query_id, template) \
                                        VALUES (?,?,?)", 
                                        [session_id, query_id, template])
                db.commit()
     
    db.close()
    return complete_sessions

main()
