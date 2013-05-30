
import matplotlib.pyplot as plt
import numpy as np

def main():

    data = read_data()
    print np.mean(data)
    print np.median(data)
    data = np.log(data) 
    n, bins, patches = plt.hist(data, 50, facecolor="green", alpha=0.75)

    locs, labels = plt.xticks()
    labels = [int(np.exp(x)) for x in range(0,10,1)]
    plt.xticks(locs, labels)
    plt.xlabel("Number of Queries Issued Per Session")
    plt.ylabel("Number of Sessions")
    plt.title("Queries per Session (Persons)")
    plt.grid(True)
    plt.show()

def read_data():
    with open('/Users/salspaugh/queryexplorer/data/queries_per_session_persons.csv') as file:
        data = []
        first = True
        for line in file.readlines():
            parts = line.split(',')
            if first:
                first = False
                continue
            data.append(int(parts[1].strip()))
    return data

main()
