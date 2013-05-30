
import math
import matplotlib.pyplot as plt
import numpy as np

from random import random

LABEL_DIST = .2
FONT_SIZE = 20.0

ARG_POINTS = "/Users/salspaugh/queryexplorer/data.storm/args/args_template_cnts_user_cnts_to_explore.csv"

def read_arg_points_to_display():
    user_counts = []
    template_counts = []
    labels = {}
    with open(ARG_POINTS) as arg_points:
        for line in arg_points.readlines():
            line = line.strip()
            if line == "":
                continue
            if line.find("#") != -1:
                continue
            parts = line.split(',')
            uc = int(parts[0])
            tc = int(parts[1])
            raw = parts[2]
            converted = raw.strip('"').lower()
            if converted in ["get", "head", "post"]:
                converted = "get|head|post"
            if converted[0:5] == "date_":
                converted = "date_*"
            if converted[0:4] == "fail":
                converted = "fail"
            if converted in ["true", "false"]:
                converted = "true|false"
            if converted.find("/var/log") == 0:
                converted = "/var/log/*"
            if converted.find("login") > -1:
                converted = "login"
            if converted.find("access") > -1:
                converted = "access_*"
            if not converted in labels:
                labels[converted] = (0,0)
            (olduc, oldtc) = labels[converted]
            labels[converted] = (olduc + uc, oldtc + tc)
    labels = list(labels.items())
    user_counts = [x[1][0] for x in labels]
    template_counts = [x[1][1] for x in labels]
    labels = [x[0] for x in labels]
    return user_counts, template_counts, labels

def read_exploratory_arg_points():
    user_counts = []
    template_counts = []
    labels = []
    with open(ARG_POINTS) as arg_points:
        for line in arg_points.readlines():
            line = line.strip()
            if line == "":
                continue
            if line.find("#") != -1:
                continue
            parts = line.split(',')
            uc = int(parts[0])
            tc = int(parts[1])
            arg = parts[2]
            if len(arg) > 9:
                continue
            #if arg in ['"*"', '"syslog"', "type", "1d", "POST", "404", "count", "title", "punct", "date_mday", "date_hour", "linecount"]:
            #    continue
            if arg in ["message", "type", "date_hour", "date_mday", "punct"]:
                continue
            user_counts.append(uc)
            template_counts.append(tc)
            labels.append(arg)
    return user_counts, template_counts, labels

def label_point(label, xp, yp):
    print "Labeling point", label, xp, yp
    plt.annotate(label, xy=(xp,yp), xytext = (0, 0), textcoords = 'offset points', size=FONT_SIZE-6.0)

def dist(p1, p2):
    return math.sqrt(((p1[0])-(p2[0]))**2 + ((p1[1])-(p2[1]))**2)

def logdist(p1, p2):
    return math.sqrt((math.log(p1[0])-math.log(p2[0]))**2 + (math.log(p1[1])-math.log(p2[1]))**2)

def too_close_to_others(new_point, taken_spots):
    for spot in taken_spots:
        if logdist(new_point, spot) < LABEL_DIST:
            return True
    return False

def adjust_points_for_spacing(x, y, labels):
    original_points = zip(x, y, labels)    
    original_points = sorted(original_points, key=lambda x: x[1])
    original_points = sorted(original_points, key=lambda x: x[0])
    new_points = []
    taken_points = []
    for (x, y, label) in original_points:
        while too_close((x,y), taken_points):
            (x, y) = (x+1, y)
        taken_points.append((x,y))
        new_points.append((x, y, label))
    x = [point[0] for point in new_points]
    y = [point[1] for point in new_points]
    labels = [point[2] for point in new_points]
    return x, y, labels

def too_close(p1, p2):
    return (logdist(p1, p2) < LABEL_DIST)

def label_where_possible(labels, x, y):
    already_labeled = []
    labeled = 0
    for label, xp, yp in zip(labels, x, y):
        nope = False
        for pnt in already_labeled:
            if too_close(pnt, (xp,yp)):
                nope = True
        if not nope:
            already_labeled.append((xp,yp))
            labeled += 1
            label_point(label, xp, yp)
    print "number of labeled points:", labeled

def label_points(labels, x, y):
    already_labeled = []
    for label, xp, yp in zip(labels, x, y):
        label_point(label, xp, yp)

def main():
    x, y, labels = read_arg_points_to_display()
    print "Read in points"
    plt.scatter(x, y, s=0)
    plt.xscale("log")
    plt.yscale("log")
    label_where_possible(labels, x, y)
    plt.xlabel("Number of query appeared in", size=FONT_SIZE)
    plt.ylabel("Number of users used by", size=FONT_SIZE)
    plt.xticks([])
    plt.yticks([])
    plt.show()

main()
