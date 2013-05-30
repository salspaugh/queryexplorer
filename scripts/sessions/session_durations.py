
import matplotlib.pyplot as plt
import numpy as np

def main():

    data = read_data()
    print np.mean(data)
    print np.median(data)
    data = [x + .0001 for x in data]
    data = np.log(data) 
    n, bins, patches = plt.hist(data, 50, facecolor="green", alpha=0.75)

    locs, labels = plt.xticks()
    labels = [int(np.exp(x)) for x in range(-15,20,5)]
    plt.xticks(locs, labels)
    plt.xlabel("Seconds per Session")
    plt.ylabel("Number of Sessions")
    plt.title("Session Duration")
    plt.grid(True)
    plt.show()

def read_data():
    with open('/Users/salspaugh/queryexplorer/data/session_durations.csv') as file:
        data = []
        first = True
        for line in file.readlines():
            parts = line.split(',')
            if first:
                first = False
                continue
            data.append(float(parts[1].strip()))
    return data

main()
