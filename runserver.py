
import sqlite3

from flask import g
from queryexplorer import app
from contextlib import closing

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    execute_db_script("schema.sql")

def execute_db_script(script):
    with closing(connect_db()) as db:
        with app.open_resource(script) as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    g.db.close()

if __name__ == "__main__":
    app.run(debug=True)
