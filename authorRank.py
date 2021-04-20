from networkx.algorithms import bipartite

from pylab import *
import json
import networkx as nx
import pandas as pd
from networkx.readwrite import json_graph
import numpy as np
import matplotlib.lines as lines
from operator import itemgetter
from fileNames import files
from TNA import TNAfunc
from FGA import FGAfunc
import multiprocessing

def authorRankFunc():
    print("Step ARC:", time.strftime("%H:%M:%S", time.localtime()))
    dataset = pd.read_csv('frequencyTest.csv', delimiter=',')
    appNames = pd.read_csv('apps_names.csv', delimiter=',')
    appN = []
    for j in appNames.values:
        if j[0] in appNames.values:
            #print("YERT",j[0])
            appN.append(j[0])

    authList = {}

    for i in range(dataset['Author'].count()):
        aVal1 = dataset['Author'][i]
        aVal2 = dataset['App'][i]
        aVal3 = dataset['Total'][i]
        authList[aVal1] = aVal2, aVal3

    T = FGAfunc()

    authorRecScores = {}
    authRecDict = {}
    edgeDict = {}

    hasEdges = False

    S = nx.Graph()

    S.add_nodes_from(T.nodes(), bipartite=0)

    print("Step 6:", time.strftime("%H:%M:%S", time.localtime()))
    for i in T:
        if len(T.edges(i)) == 0:
            #print(i, " has no recommendations")
            edgeDict[i] = False
        else:
            #print(i)
            edgeDict[i] = True

    #print(edgeDict)
    tempDict = {}
    tempArr = []
    yes = {}

    print("Step 7:", time.strftime("%H:%M:%S", time.localtime()))
    for i in T:

        if edgeDict[i] == True:
            for j in T.edges(i):
                #print(i,"what",j[1])
                if T.has_edge(i, j[1]):
                    tempDict[j[1]] = j[1],T[i][j[1]]['weight'],authList[j[1]][0]
                    #print(i)
                    tempArr.append(tempDict[j[1]])
                    #print("what the fuck", tempArr)
            yes = tempArr
            authRecDict[i] = tempArr
            #print("HYFR",i,"\n",authRecDict[i])
        tempArr = []
        tempDict = {}

        #print("WHAAAAAAT", authRecDict)

    #print(yes, "oh fuck", authRecDict)

    scores = []
    appNTrim = []

    #for k in appN:
        #if k in authRecDict:
            #appNTrim.append(k)
            #print("HEY YEAH",appNTrim)
    appNTrim = set(appNTrim)
    appNTrim = list(appNTrim)

    #print(appNTrim)

    S.add_nodes_from(appN, bipartite=1)

    authListTrim = []

    print("Step 8:", time.strftime("%H:%M:%S", time.localtime()))
    for i in authRecDict:
        #print(i,"yo",authRecDict[i])
        authListTrim.append(i)
        for j in authRecDict[i]:
            #print(j)
            #print("yoyoyoyoyo"+authRecDict[i][j][2])
            for k in appN:
                #print("yooooooooo",j[2])
                if k in j[2] and k not in authList[i][0]:
                    #appNTrim.append(k)
                    #print(i,k,"AHHHHHHHH",j[0],"OKAYOKAYOKAY",j[2],"SO TIRED",authList[i][0])
                    scores.append(j[1])
                    if S.has_edge(i, k):# and j[1] > S[i][k]["weight"]:
                        S[i][k]["weight"] = (S[i][k]["weight"] + j[1]) / 2
                    else:
                        S.add_edge(i, k, weight=j[1])
                    #print(k,"okay")

    #print(appNames.values)
    #print("done")

    S.remove_nodes_from(list(nx.isolates(S)))

    #####################################################
    #####################################################hEdgeCount = {}
    #####################################################for f in S.nodes:
        #####################################################hEdgeCount[f] = len(S.edges(f))
    #####################################################

    #####################################################nodeWeight = [float(l) * 20 for x, l in hEdgeCount.items()]

    # Map to layout #####################################################
    #####################################################plt.clf()
    #pos = nx.spring_layout(S, k=0.85, iterations=20, scale=10)
    #####################################################pos = nx.bipartite_layout(S, T.nodes())
    #pos = nx.circular_layout(S)
    #print(nx.info(S))
    #####################################################plt.figure(1, figsize=(100, 100))
    #####################################################

    #for i in list(nx.isolates(S)):
        #S.remove_node(list(nx.isolates(S))[i])

    #print(list(nx.isolates(S)))

    #print("YALL",appN)

    print("Step 9:", time.strftime("%H:%M:%S", time.localtime()))

    ##########################################################################
    ###nx.draw_networkx_nodes(S, pos=pos, node_color="red")#, node_size=nodeWeight)
    ###nx.draw_networkx_nodes(S, pos=pos, node_color="green", nodelist=authListTrim)#, node_size=nodeWeight)
    ###nx.draw_networkx_edges(S, pos=pos)#, width=scores)
    ##########################################################################

    #print(multiprocessing.cpu_count())

    # Print graph list to output, and output image
    #graphDictionaryFile.write(str(S.edges))
    plt.savefig("AuthorRankAnalysis.jpg")

    nx.write_gpickle(S, "S_COMPLETE.gpickle")

    # convert array into dataframe
    DF = pd.DataFrame(authListTrim)

    # save the dataframe as a csv file
    DF.to_csv("authorListTrimmed.csv", header=False, index=False)

    #np.savetxt('authorListTrimmed.csv', authListTrim, delimiter=',')

    #print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!",S.has_edge("A Ford","AlphaBetty Saga"))

    print("Step 10:", time.strftime("%H:%M:%S", time.localtime()))
    data = json_graph.node_link_data(S)
    s1 = json.dumps(data)
    with open('RV.json', 'w', encoding='utf-8') as f:
        f.write(s1)

    print("Step 11:", time.strftime("%H:%M:%S", time.localtime()))
    # Return graph to call function
    return S, authListTrim, appN