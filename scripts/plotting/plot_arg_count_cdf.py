
import matplotlib.pyplot as plt
import numpy as np
from queryexplorer import connect_db

def main():
    counts = []
    #labels = []
    db = connect_db()
    #cursor = db.execute("SELECT count(*) AS cnt, arg FROM args GROUP BY arg ORDER BY cnt DESC")
    cursor = db.execute("select count(distinct queries.user_id) as cnt, arg from args, queries where args.query_id = queries.id group by arg order by cnt desc")
    for (cnt, arg) in cursor.fetchall():
        counts.append(cnt)
        #labels.append(arg)
    db.close()    

    #counts = np.log(counts)
    ind = range(max(counts)+1)
    #ind = np.logspace(0, np.log10(max(counts)), num=20)
    #ind = [0] + list(ind)
    #ind = np.linspace(0, max(counts), num=20)
    #print ind
    total = len(counts) 
    cdf = [float(len(filter(lambda x: x <= i, counts)))/float(total) for i in ind]
    #print zip(ind, cdf)
    plt.plot(ind, cdf)
    plt.ylabel("Percent of arguments with counts less than or equal to C")
    plt.xlabel("C")
    plt.xscale("log")
    plt.grid(True)
    plt.show()

main()
