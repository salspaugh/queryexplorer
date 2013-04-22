#!/usr/bin/env python

import json
from splparser.parsetree import ParseTreeNode

def main():

    data = read_data()
    for (cnt, template) in data:
        template.print_tree()
        print "count: ", cnt
        print "" 
        print ""

def read_data():
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
