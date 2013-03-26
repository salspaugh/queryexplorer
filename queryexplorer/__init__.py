from flask import Flask

DATABASE = 'queryexplorer.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)

import queryexplorer.api
import queryexplorer.views
