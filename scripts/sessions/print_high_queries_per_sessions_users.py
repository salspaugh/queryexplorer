#!/usr/bin/env python

from queryexplorer import connect_db

def main():
    
    db = connect_db()
    big_sessions_cursor = db.execute("SELECT session_id, COUNT(session_id) AS cnt FROM queries GROUP BY session_id ORDER BY cnt DESC")
    for (session_id, queries_per_session) in big_sessions_cursor.fetchall():
        if queries_per_session > 30:
            session_owner_cursor = db.execute("SELECT user_id FROM sessions WHERE id=? LIMIT 1", [session_id])
            user_id = session_owner_cursor.fetchall()[0][0]
            owner_name_cursor = db.execute("SELECT name, user_type FROM users WHERE id=? LIMIT 1", [user_id])
            for (name, user_type) in owner_name_cursor.fetchall():
                if user_type == "person":
                    print ','.join([str(name), str(session_id), str(queries_per_session)])
    db.close()


main()
