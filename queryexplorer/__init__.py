from flask import Flask, request, session, g, redirect, url_for, abort, render_template
import sqlite3

DATABASE = 'queryexplorer.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)

import queryexplorer.views
