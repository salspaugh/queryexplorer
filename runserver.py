
import sqlite3

from queryexplorer import app
from contextlib import closing

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()

if __name__ == "__main__":
    app.run(debug=True)
