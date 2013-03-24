
import json

from flask import render_template
from queryexplorer import app

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/stats')
def basic_stats():
    '''
    {
        "dataset" : "Users" | "Splunk user queries" | "Sessions" | "Splunk application queries",
        "count" : "<number>",
    }
    '''
    #cur = g.db.execute('')
    fake = []
    fake.append({"dataset": "Users", "count": 5})
    fake.append({"dataset": "Splunk user queries", "count": 15})
    fake.append({"dataset": "Sessions", "count": 5})
    return json.dumps(fake, sort_keys=False) 

@app.route('/commands_indicator')
def commands_indicator_visualization():
    return render_template('commands_indicator.html')

#@app.route('/commands_versus_arguments')

#@app.route('/queries')

#@app.route('/queries/<query_id>')

#@app.route('/users/<user_id>')

#@app.route('/sessions')

#@app.route('/sessions/<session_id>')


