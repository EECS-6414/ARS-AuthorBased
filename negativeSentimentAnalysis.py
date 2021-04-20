import pandas
from pylab import *
import networkx as nx
import pandas as pd
import matplotlib.lines as mlines
from operator import itemgetter
from collections import OrderedDict
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import matplotlib.patches as mpatches
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

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

    #print(countList)

    commentCount = list(countList.keys())

    #print(commentCount)

    #commentCount = list(countList.values())

    #print(totalUserCount)

    for i in countList:
    #    print(i)
    #    print(countList.get(i))
    #    commentCount.append(i)
         totalUserCount.append(countList.get(i))
    #    print(commentCount)
         #print(totalUserCount)

    #df = pd.DataFrame(np.random.rand(10, 27), columns=commentCount)

    #df.plot.area()

    #fig, ax = plt.subplots()

    #ax.bar(commentCount, totalUserCount, width=1, label='Total Count')#, yerr=men_std)
    #ax.bar(commentCount, women_means, width, yerr=women_std, bottom=men_means, label='Women')

    #ax.set_ylabel('Total Numbers of Users')
    #ax.set_xlabel('Total Numbers of Comments')
    #ax.set_title('Negative Sentiment')
    #ax.legend()

    #plt.show()

#    try:
#        geeky_file = open('fullCount.txt', 'wt')
#        geeky_file.write(str(countList))
#        geeky_file.close()
#        print("\nSuccessfully Saved File")
#
#    except:
#        print("Unable to write to file")
#
    return countList


#def fullCount():
#    Y = nx.read_gpickle("G_COMPLETE.gpickle")
#    appNames = pd.read_csv('apps_names.csv', delimiter=',')
#
#    countDict = {}
#
#    positiveAuthList = []
#
#    # Add nodes to H based on binary sentiment output
#    #print(Y.number_of_edges())
#    for u in Y:
#        nodeAdded = False
#        #for j in appNames.values:
#        #if nodeAdded == True:
#                #nodeAdded = False
#            #break
#        #print("0")
#        if u in appNames.values:
#            continue
#            #print("1")
#            #if Y.has_edge(j[0], u):
#        if len(Y.edges(u)) not in countDict.keys():
#            #print("2")
#            countDict[len(Y.edges(u))] = 1
#        else:
#            countDict[len(Y.edges(u))] += 1
#            #print("3")
#                #nodeAdded = True
#
#    print(countDict)
#
#    return countDict



def positiveSentiment(path, names, countDict):
    Y = nx.read_gpickle("G_COMPLETE.gpickle")
    appNames = pd.read_csv('apps_names.csv', delimiter=',')

    #countDictNew = countDict.copy()

    countDictNew = {}

    positiveAuthList = []

    # Add nodes to H based on binary sentiment output
    for u in Y:
        nodeAdded = False
        # print("No way", u)
        for j in appNames.values:
            if nodeAdded == True:
                break
            if u in appNames.values:
                # print("No way", u)
                break
            #print(j[0])
            # print(u)
            if Y.has_edge(j[0], u):
                if 'b' == Y[u][j[0]]['color']:# or 'k' == Y[u][j[0]]['color']:
                    #print("Here")
                    nodeAdded = True
                    if len(Y.edges(u)) not in countDictNew.keys():
                        #print("There")
                        countDictNew[len(Y.edges(u))] = 0
                    else:
                        #print("3")
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
        #else:
        #    negativeCount[i] = 100.0

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
    #print(val1Labels)

    userCount1 = []

    for i in val1:
        userCount1.append(val1.get(i))

    #print(userCount1)

    val2Labels = list(val2.keys())
    #print(val2Labels)

    userCount2 = []

    for i in val2:
        userCount2.append(val2.get(i))

    #print(userCount2)

    val3Labels = list(val3.keys())
    #print(val3Labels)

    userCount3 = []

    for i in val3:
        userCount3.append(val3.get(i))

    #print(userCount3)



    ax.bar(val1Labels, userCount1, width=1, label='Total User Count')  # , yerr=men_std)
    ax.bar(val2Labels, userCount2, width=1, label='Blended Sentiment User Count')

    ax2 = ax.twinx()
    ax2.plot(val3Labels, userCount3, color="C3", marker="D", ms=7)
    ax2.yaxis.set_major_formatter(PercentFormatter())

    #ax.stackplot(val1Labels, userCount1, labels=val1Labels)
    #ax.stackplot(val2Labels, userCount2, labels=val2Labels)

    handles, labels = ax.get_legend_handles_labels()
    patch = mpatches.Patch(color='red', label='% of Purely Negative Users')
    handles.append(patch)
    plt.legend(handles=handles, loc='center right')

    ax.set_ylabel('Number of Users')
    ax.set_xlabel('Number of Comments per User')
    ax.set_title('Negative Sentiment Analysis')
    #ax.legend(loc='center right')
    #ax2.legend(loc='lower right')

    plt.savefig('negativeSentiment.eps', format='eps')
    plt.savefig('negativeSentiment.jpg', format='jpg')

    plt.show()