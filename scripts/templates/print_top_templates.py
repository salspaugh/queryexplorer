#!/usr/bin/env python

import json
from queryexplorer import connect_db
from splparser.parsetree import ParseTreeNode

def main():

    db = connect_db()
    cursor = db.execute("select count(distinct users.name) as cnt, template from templates, users, queries where templates.query_id = queries.id and queries.user_id = users.id group by template order by cnt desc")
    data = cursor.fetchall() 
    for (cnt, template) in data:
        d = json.loads(template)
        template = ParseTreeNode.from_dict(d)
        template.print_tree()
        print "count: ", cnt
        print "" 
        print ""
    db.close()
    

def read_csv_data():
    with open('/Users/salspaugh/queryexplorer/data/top_templates.csv') as file:
        data = []
        first = True
        for line in file.readlines():
            parts = line.split(',')
            if first:
                first = False
                continue
            cnt = int(parts[0])
            jsonified_tree = ','.join(parts[1:])
            d = json.loads(jsonified_tree)
            template = ParseTreeNode.from_dict(d)
            data.append((cnt, template))
    return data

main()
