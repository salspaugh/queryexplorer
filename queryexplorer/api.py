
import json
import math
import time

from flask import g, request
from queryexplorer import app

@app.route('/stats')
def basic_stats():
    '''
    {
        "dataset" : "Users" | "Splunk user queries" | "Sessions" | "Splunk application queries",
        "count" : "<number>",
    }
    '''
    stats = []
    cursor = g.db.execute("SELECT count(*) FROM queries")
    query_count = cursor.fetchall()[0]
    print query_count
    cursor = g.db.execute("SELECT count(*) FROM users")
    user_count = cursor.fetchall()[0]
    cursor = g.db.execute("SELECT count(*) FROM sessions")
    session_count = cursor.fetchall()[0]
    stats.append({"dataset": "Splunk user queries", "count": query_count})
    stats.append({"dataset": "Users", "count": user_count})
    stats.append({"dataset": "Sessions", "count": session_count})
    return json.dumps(stats, sort_keys=False) 

@app.route('/commands_indicator_coordinates')
def command_indicator_visualization_coordinates():
    start = time.time()
    cursor = g.db.execute("SELECT rowidx, colidx, command, hash, indicator_group_id, class \
                            FROM commands_indicator_coordinates")
    executed_select = time.time()
    print "Executed select in", executed_select - start
    rectangle_coordinates = [dict(zip(['ridx', 'cidx', 'cmd', 'hash', 'group_id', 'class'], row)) 
                                for row in cursor.fetchall()]
    composed_dicts = time.time()
    print "Composed dicts in", composed_dicts - executed_select
    return json.dumps(rectangle_coordinates) 

@app.route('/commands_indicator_class', methods=['POST'])
def commands_indicator_class():
    if request.method == 'POST':
        group_id = int(request.form['group_id'])
        cls = request.form['label']
        cursor = g.db.cursor()
        cursor.execute("UPDATE queries SET class=? WHERE commands_indicator_group_id=?", [cls, group_id])
        g.db.commit()
    return "Successfully posted to /commands_indicator_class\n"
