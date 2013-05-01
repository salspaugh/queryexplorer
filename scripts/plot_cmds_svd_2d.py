
import json
import math
import matplotlib.pyplot as plt

CMDS_2D = "/Users/salspaugh/queryexplorer/data/svd/scaled_cmds2d.csv"
CMDS_LABELS = "/Users/salspaugh/queryexplorer/data/svd/cmd_col_matrix_labels.csv"
LABEL_DIST = 1

def read_cmd_points():
    x = []
    y = []
    first = True
    with open(CMDS_2D) as cmds2dfile:
        for line in cmds2dfile.readlines():
            if first: 
                first = False
                continue
            parts = line.split(',')
            x.append(float(parts[1]))
            y.append(float(parts[2]))
    return x,y

def read_cmd_labels():
    cmd_labels = {}
    with open(CMDS_LABELS) as cmdslabelsfile:
        for line in cmdslabelsfile.readlines():
            (idx, label) = json.loads(line)
            cmd_labels[idx] = label
    return map(lambda x: x[1], sorted(cmd_labels.items(), key=lambda x: x[0]))

def label_point(label, xp, yp):
    print "Labeling point", xp, yp, "with label", label
    plt.annotate(label, xy=(xp,yp), xytext = (-5, 5), textcoords = 'offset points')

def dist(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def too_close(p1, p2):
    return (dist(p1, p2) < LABEL_DIST)

def label_where_possible(labels, x, y):
    already_labeled = []
    for label, xp, yp in zip(labels, x, y):
        nope = False
        for pnt in already_labeled:
            if too_close(pnt, (xp,yp)):
                nope = True
        if not nope:
            already_labeled.append((xp,yp))
            label_point(label, xp, yp)

def main():
    x,y = read_cmd_points()
    print "Read in points"
    labels = read_cmd_labels()
    print "Read in labels"
    plt.scatter(x, y)
    plt.grid(True)
    label_where_possible(labels, x, y)
    plt.show()

main()

