#!/usr/bin/env python

import json
from splparser.parsetree import ParseTreeNode

def main():

    data = read_data()
    for (template_cnt, user_cnt, template) in data:
        template.print_tree()
        print "template count: ", template_cnt
        print "user count: ", user_cnt
        print "" 
        print ""

def read_data():
    with open('/Users/salspaugh/queryexplorer/data/popular_templates.csv') as file:
        data = []
        first = True
        for line in file.readlines():
            parts = line.split(',')
            if first:
                first = False
                continue
            template_cnt = int(parts[0])
            user_cnt = int(parts[1])
            jsonified_tree = ','.join(parts[2:])
            d = json.loads(jsonified_tree)
            template = ParseTreeNode.from_dict(d)
            data.append((template_cnt, user_cnt, template))
    return data

main()
