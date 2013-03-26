
import json
import math

from flask import g
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
    cursor = g.db.execute('SELECT count(*) FROM queries')
    query_count = cursor.fetchall()[0]
    print query_count
    cursor = g.db.execute('SELECT count(*) FROM users')
    user_count = cursor.fetchall()[0]
    cursor = g.db.execute('SELECT count(*) FROM sessions')
    session_count = cursor.fetchall()[0]
    stats.append({"dataset": "Splunk user queries", "count": query_count})
    stats.append({"dataset": "Users", "count": user_count})
    stats.append({"dataset": "Sessions", "count": session_count})
    return json.dumps(stats, sort_keys=False) 

@app.route('/commands_indicator_coordinates')
def command_indicator_visualization_coordinates():
    cursor = g.db.execute('SELECT count(*), indicator_vector \
                            FROM command_indicators \
                            GROUP BY indicator_vector \
                            ORDER BY indicator_vector')
    rectangle_coordinates = []
    xrange = 0
    for (count, feature_string) in cursor.fetchall():
        for i in range(int(max(1, round(math.log(count))))):
            for j in range(len(feature_string)):
                if feature_string[j] == '1':
                    cmd = g.db.execute('SELECT command \
                                            FROM command_indicator_key \
                                            WHERE idx = ?', str(j)).fetchall()[0][0]
                    coords = {}
                    coords['ridx'] = xrange
                    coords['cidx'] = j 
                    coords['cmd'] = cmd 
                    hash = ''.join([str(x) for x in coords.values()])
                    coords['hash'] = hash
                    rectangle_coordinates.append(coords)
        xrange += 1
    return json.dumps(rectangle_coordinates)
