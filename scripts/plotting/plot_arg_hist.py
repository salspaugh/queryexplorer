
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

    ind = range(len(counts))
    counts = np.log(counts)
    print counts[0:20]
    #width = 1.0
    #bars = plt.bar(ind, counts, width, color="green", alpha=0.5)
    plt.plot(ind, counts)
    plt.ylabel("log( Number of times argument appears )")
    plt.xlabel("Argument rank")
    #plt.xticks(rotation=90)
    #plt.xticks([i+width/2 for i in ind], labels)
    plt.grid(True)
    plt.show()

main()
