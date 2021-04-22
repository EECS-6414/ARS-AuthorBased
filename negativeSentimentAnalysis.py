import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import matplotlib.patches as mpatches

def fullCount():
    # Open input csv file, and create output files
    dataset = pd.read_csv('frequencyTest.csv', delimiter=',')

    countList = {}

    print("\nStarting Count")

    for i in range(dataset['App'].count()):
        aVal = dataset['App'][i]
        maxVal = 30

        parts = aVal.split(";")
        if len(parts) in countList and len(parts) < maxVal:
            countList[len(parts)] += 1
        elif len(parts) < maxVal:
            countList[len(parts)] = 1

    countList = countList.items()

    countList = sorted(countList)

    countList = dict(countList)

    commentCount = []
    totalUserCount = []

    commentCount = list(countList.keys())

    for i in countList:
        totalUserCount.append(countList.get(i))

    return countList

def positiveSentiment(path, names, countDict):
    Y = nx.read_gpickle("G_COMPLETE.gpickle")
    appNames = pd.read_csv('apps_names.csv', delimiter=',')

    countDictNew = {}

    positiveAuthList = []

    # Add nodes to H based on binary sentiment output
    for u in Y:
        nodeAdded = False
        for j in appNames.values:
            if nodeAdded == True:
                break
            if u in appNames.values:
                break
            if Y.has_edge(j[0], u):
                if 'b' == Y[u][j[0]]['color']:# or 'k' == Y[u][j[0]]['color']:
                    nodeAdded = True
                    if len(Y.edges(u)) not in countDictNew.keys():
                        countDictNew[len(Y.edges(u))] = 0
                    else:
                        countDictNew[len(Y.edges(u))] += 1

    print(countDictNew)

    return countDictNew

def negativeAnalysis(val1, val2):

    negativeCount = {}

    print("Val:", val1, val2)

    for i in val1:
        if i in val2.keys():
            if val1.get(i) > val2.get(i):
                negativeCount[i] = round(((val1.get(i) - val2.get(i)) / val1.get(i)) * 100, 2)
            elif val1.get(i) == 0:
                negativeCount[i] = 0.0
            else:
                negativeCount[i] = 0.0

    negativeCountOrdered = {}

    keyListOrdered = list(negativeCount.keys())

    keyListOrdered.sort()

    print(keyListOrdered)

    for i in keyListOrdered:
        negativeCountOrdered[i] = negativeCount[i]

    print(negativeCountOrdered)

    return negativeCountOrdered

def printNegativeAnalysis(val1, val2, val3):
    fig, ax = plt.subplots()

    val1Labels = list(val1.keys())

    userCount1 = []

    for i in val1:
        userCount1.append(val1.get(i))

    val2Labels = list(val2.keys())

    userCount2 = []

    for i in val2:
        userCount2.append(val2.get(i))

    val3Labels = list(val3.keys())

    userCount3 = []

    for i in val3:
        userCount3.append(val3.get(i))

    ax.bar(val1Labels, userCount1, width=1, label='Total User Count')  # , yerr=men_std)
    ax.bar(val2Labels, userCount2, width=1, label='Blended Sentiment User Count')

    ax2 = ax.twinx()
    ax2.plot(val3Labels, userCount3, color="C3", marker="D", ms=7)
    ax2.yaxis.set_major_formatter(PercentFormatter())

    handles, labels = ax.get_legend_handles_labels()
    patch = mpatches.Patch(color='red', label='% of Purely Negative Users')
    handles.append(patch)
    plt.legend(handles=handles, loc='center right')

    ax.set_ylabel('Number of Users')
    ax.set_xlabel('Number of Comments per User')
    ax.set_title('Negative Sentiment Analysis')

    plt.savefig('negativeSentiment.eps', format='eps')
    plt.savefig('negativeSentiment.jpg', format='jpg')

    plt.show()