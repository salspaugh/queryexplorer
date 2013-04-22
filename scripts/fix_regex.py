#!/usr/bin/env python

from queryexplorer import connect_db

def main():
    db = connect_db()
    select_cursor = db.execute("SELECT id, text FROM queries WHERE id<?", [31651])
    for (id, query) in select_cursor.fetchall():
        if query.find(' rex ') > -1:
            delete_template_commands_args(db, id)
    db.close()

def delete_template_commands_args(db, id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM templates WHERE query_id=?", [id])
    cursor.execute("DELETE FROM commands WHERE query_id=?", [id])
    cursor.execute("DELETE FROM args WHERE query_id=?", [id])
    db.commit()

main()
