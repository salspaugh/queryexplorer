
import sqlite3

from queryexplorer import app, connect_db
from queryutils import get_user_sessions, CommandsIndicatorFeatureVector, Query
from contextlib import closing

BYTES_IN_MB = 1048576

db = None

def init_db():
    execute_db_script("schema.sql")

def execute_db_script(script):
    with closing(connect_db()) as db:
        with app.open_resource(script) as f:
            db.cursor().executescript(f.read())
        db.commit()

def load_db():
    global db
    db = connect_db()
    user_id = 1
    session_id = 1
    query_id = 1
    commands_indicator_feature_id = 1
    for users in get_user_sessions(limit=3*BYTES_IN_MB): 
        for user in users:
            print "loaded user"
            insert_user(user_id, user.name)
            for (local_sid, session) in user.sessions.iteritems(): 
                insert_session(session_id, user_id)
                for query in session.queries:
                    vector = CommandsIndicatorFeatureVector(query_id, query).values_as_bit_string()
                    insert_query(query_id, query.text, query.time, False, user_id, session_id=session_id)
                    insert_commands_indicator_feature(commands_indicator_feature_id, vector, query_id)
                    commands_indicator_feature_id += 1
                    query_id += 1
                session_id += 1
            for query in user.autorecurring_queries:
                vector = CommandsIndicatorFeatureVector(query_id, query).values_as_bit_string()
                insert_query(query_id, query.text, query.time, True, user_id)
                insert_commands_indicator_feature(commands_indicator_feature_id, vector, query_id)
                commands_indicator_feature_id += 1
                query_id += 1
            user_id += 1
    empty_query = Query("", 0, "", "")
    empty_vector = CommandsIndicatorFeatureVector(0, empty_query)
    for (cmd, idx) in empty_vector.command_index_tuples():
        insert_commands_indicator_key(cmd, idx)
    db.close()

def insert_user(id, username):
    cursor = db.cursor()
    cursor.execute("INSERT INTO users (id, name) VALUES (?,?)", [id, username])
    db.commit() 

def insert_session(id, userid):
    cursor = db.cursor()
    cursor.execute("INSERT INTO sessions (id, user_id) VALUES (?,?)", [id, userid])
    db.commit()

def insert_query(id, text, time, autogenerated, user_id, session_id=None):
    cursor = db.cursor()
    if session_id is not None:
        cursor.execute("INSERT INTO queries \
                            (id, text, time, autogenerated, user_id, session_id) \
                            VALUES (?,?,?,?,?,?)", 
                            [id, text, time, autogenerated, user_id, session_id])
    else:
        cursor.execute("INSERT INTO queries \
                            (id, text, time, autogenerated, user_id) \
                            VALUES (?,?,?,?,?)",
                            [id, text, time, autogenerated, user_id])
    db.commit()

def insert_commands_indicator_feature(id, vector, query_id):
    cursor = db.cursor()
    cursor.execute("INSERT INTO commands_indicators \
                        (id, indicator_vector, query_id) VALUES (?,?,?)", 
                        [id, vector, query_id])
    db.commit() 

def insert_commands_indicator_key(command, index):
    cursor = db.cursor()
    cursor.execute("INSERT INTO commands_indicator_key (command, idx) VALUES (?,?)", [command, index])
    db.commit()
