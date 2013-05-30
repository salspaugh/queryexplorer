#!/usr/bin/env python

import queryutils
import re
import sys

from collections import defaultdict
from queryexplorer import connect_db

def main():
    db = connect_db()
    select_cursor = db.execute("SELECT id, name FROM users")
    for (id, name) in select_cursor.fetchall():
        matches = re.findall('[\d]{9}', name)
        if len(matches) > 0:
            update_user_type_as_machine(db, id)
        matches = re.findall('[a-z]{2}[\d]{5}', name)
        if len(matches) > 0:
            update_user_type_as_machine(db, id)
        matches = re.findall('[a-z]{1}[\d]{6}', name)
        if len(matches) > 0:
            update_user_type_as_machine(db, id)
        matches = re.findall('\d[a-z]{5}\d', name)
        if len(matches) > 0:
            update_user_type_as_machine(db, id)
        matches = re.findall('[a-z]{2}[\d]{3}[a-z]', name)
        if len(matches) > 0:
            update_user_type_as_machine(db, id)
        matches = re.findall('[\d][a-z]{5}\d', name)
        if len(matches) > 0:
            update_user_type_as_machine(db, id)
        matches = re.findall('savedsearch', name)
        if len(matches) > 0:
            update_user_type_as_machine(db, id)
        matches = re.findall('[\d]{8}', name)
        if len(matches) > 0:
            update_user_type_as_machine(db, id)
    db.close()

def update_user_type_as_machine(db, id):
    cursor = db.cursor()
    cursor.execute('UPDATE users SET user_type="machine" where id=?', [id])
    db.commit()

main()
