
import inspect
import sys

from flask import render_template, url_for
from queryexplorer import app
from queryexplorer.decorators import view

def get_navigation_elements():
    functions = [x for x in globals().values() 
                    if (inspect.isfunction(x) and 
                            inspect.getmodule(x) == sys.modules[__name__])] 
    function_names = []
    for function in functions:
        try:
            if function.is_view:
                function_names.append(function.__name__)
        except AttributeError:
            pass
    navigation_links = [url_for(x) 
                                for x in function_names]
    navigation_text = [x.lstrip('/').replace('_', ' ').title() 
                                for x in navigation_links]
    navigation_elements = []
    for (link, text) in zip(navigation_links, navigation_text):
        navigation_elements.append({'link': link, 'text': text})
    return navigation_elements

def render_template_with_navigation(template):
    return render_template(template, navigation_elements=get_navigation_elements())

@view
@app.route('/')
def index():
    return render_template_with_navigation('index.html') 

@view
@app.route('/commands_indicator')
def commands_indicator_visualization():
    return render_template_with_navigation('commands_indicator.html')

@view
@app.route('/commands_versus_arguments')
def commands_versus_arguments_visualization():
    return render_template_with_navigation('commands_versus_arguments.html')

#@app.route('/queries')

#@app.route('/queries/<query_id>')

#@app.route('/users/<user_id>')

#@app.route('/sessions')

#@app.route('/sessions/<session_id>')


