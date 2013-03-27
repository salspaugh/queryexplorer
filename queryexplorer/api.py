
import json
import math

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
    cursor = g.db.execute("SELECT count(*), GROUP_CONCAT(query_id), indicator_vector \
                            FROM commands_indicators \
                            GROUP BY indicator_vector \
                            ORDER BY indicator_vector")
    rectangle_coordinates = []
    xrange = 0
    group_id = 0
    for (count, query_id_list, feature_string) in cursor.fetchall():
        for query_id in query_id_list.split(','):
            cursor = g.db.cursor()
            cursor.execute('UPDATE queries SET commands_indicator_viz_group=? WHERE id=?', [group_id, query_id])
            g.db.commit()
        for i in range(int(max(1, round(math.log(count))))):
            for j in range(len(feature_string)):
                if feature_string[j] == '1':
                    cmd = g.db.execute("SELECT command \
                                            FROM commands_indicator_key \
                                            WHERE idx=?", str(j)).fetchall()[0][0]
                    cls = g.db.execute("SELECT class FROM queries \
                                            WHERE id=?", str(query_id)).fetchall()[0][0]
                    coords = {}
                    coords['ridx'] = xrange
                    coords['cidx'] = j 
                    coords['cmd'] = cmd 
                    hash = ''.join([str(x) for x in coords.values()])
                    coords['hash'] = hash
                    coords['group_id'] = group_id 
                    coords['class'] = cls
                    rectangle_coordinates.append(coords)
        xrange += 1
        group_id += 1
    return json.dumps(rectangle_coordinates)

@app.route('/commands_indicator_class', methods=['POST'])
def commands_indicator_class():
    if request.method == 'POST':
        group_id = int(request.form['group_id'])
        cls = request.form['label']
        print cls, group_id
        cursor = g.db.cursor()
        cursor.execute("UPDATE queries SET class=? WHERE commands_indicator_viz_group=?", [cls, group_id])
        g.db.commit()
    return "Successfully posted to /commands_indicator_class\n"
