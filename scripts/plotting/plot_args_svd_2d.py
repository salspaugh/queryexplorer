
import json
import math
import matplotlib.pyplot as plt

ARGS_2D = "/Users/salspaugh/queryexplorer/data.storm/svd/tfidf_args2d.csv"

ARGS_LABELS = "/Users/salspaugh/queryexplorer/data.storm/svd/arg_row_matrix_labels_tfidf.csv"

LABEL_DIST = 1

def read_arg_points():
    x = []
    y = []
    first = True
    with open(ARGS_2D) as args2dfile:
        for line in args2dfile.readlines():
            if first: 
                first = False
                continue
            parts = line.split(',')
            x.append(float(parts[1]))
            y.append(float(parts[2]))
    return x,y

def read_arg_labels():
    arg_labels = {}
    with open(ARGS_LABELS) as argslabelsfile:
        for line in argslabelsfile.readlines():
            (idx, label) = json.loads(line)
            arg_labels[idx] = label
    return map(lambda x: x[1], sorted(arg_labels.items(), key=lambda x: x[0]))

def label_point(label, xp, yp):
    print "Labeling point", xp, yp
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
    x,y = read_arg_points()
    print "Read in", len(x), "points"
    labels = read_arg_labels()
    print "Read in labels"
    plt.scatter(x, y)
    plt.grid(True)
    label_where_possible(labels, x, y)
    plt.show()

main()

