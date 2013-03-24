
import inspect
import json
import sys

from flask import render_template, url_for
from queryexplorer import app

@app.route('/')
def index():
    functions = filter(lambda x: inspect.isfunction(x), globals().values()) 
    functions = filter(lambda x: inspect.getmodule(x) == sys.modules[__name__], functions)
    navigation_links = [url_for(x.__name__) 
                                for x in functions]
    navigation_text = [x.lstrip('/').replace('_', ' ').title() 
                                for x in navigation_links]
    navigation_elements = []
    for (link, text) in zip(navigation_links, navigation_text):
        navigation_elements.append({'link': link, 'text': text})
    print navigation_elements
    return render_template('index.html', navigation_elements=navigation_elements) 

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

@app.route('/commands_versus_arguments')
def commands_versus_arguments_visualization():
    pass

#@app.route('/queries')

#@app.route('/queries/<query_id>')

#@app.route('/users/<user_id>')

#@app.route('/sessions')

#@app.route('/sessions/<session_id>')


