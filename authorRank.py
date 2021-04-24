from pylab import *
import json
import networkx as nx
import pandas as pd
from networkx.readwrite import json_graph
from FGA import FGAfunc

def authorRankFunc():
    print("Step ARC:", time.strftime("%H:%M:%S", time.localtime()))
    dataset = pd.read_csv('frequencyTest.csv', delimiter=',')
    appNames = pd.read_csv('apps_names.csv', delimiter=',')
    appN = []
    for j in appNames.values:
        if j[0] in appNames.values:
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
            edgeDict[i] = False
        else:
            edgeDict[i] = True

    tempDict = {}
    tempArr = []
    yes = {}

    print("Step 7:", time.strftime("%H:%M:%S", time.localtime()))
    for i in T:

        if edgeDict[i] == True:
            for j in T.edges(i):
                if T.has_edge(i, j[1]):
                    tempDict[j[1]] = j[1],T[i][j[1]]['weight'],authList[j[1]][0]
                    tempArr.append(tempDict[j[1]])
            yes = tempArr
            authRecDict[i] = tempArr
        tempArr = []
        tempDict = {}

    scores = []
    appNTrim = []

    appNTrim = set(appNTrim)
    appNTrim = list(appNTrim)

    S.add_nodes_from(appN, bipartite=1)

    authListTrim = []

    print("Step 8:", time.strftime("%H:%M:%S", time.localtime()))
    for i in authRecDict:
        authListTrim.append(i)
        for j in authRecDict[i]:
            for k in appN:
                if k in j[2] and k not in authList[i][0]:
                    scores.append(j[1])
                    if S.has_edge(i, k):# and j[1] > S[i][k]["weight"]:
                        S[i][k]["weight"] = (S[i][k]["weight"] + j[1]) / 2
                    else:
                        S.add_edge(i, k, weight=j[1])

    S.remove_nodes_from(list(nx.isolates(S)))

    # Map to layout #####################################################
    #plt.clf()
    #pos = nx.spring_layout(S, k=0.85, iterations=20, scale=10)
    #pos = nx.bipartite_layout(S, T.nodes())
    #pos = nx.circular_layout(S)
    #print(nx.info(S))
    #plt.figure(1, figsize=(100, 100))
    #####################################################

    print("Step 9:", time.strftime("%H:%M:%S", time.localtime()))

    ##########################################################################
    ###nx.draw_networkx_nodes(S, pos=pos, node_color="red")#, node_size=nodeWeight)
    ###nx.draw_networkx_nodes(S, pos=pos, node_color="green", nodelist=authListTrim)#, node_size=nodeWeight)
    ###nx.draw_networkx_edges(S, pos=pos)#, width=scores)
    ##########################################################################

    plt.savefig("AuthorRankAnalysis.jpg")

    nx.write_gpickle(S, "S_COMPLETE.gpickle")

    # convert array into dataframe
    DF = pd.DataFrame(authListTrim)

    # save the dataframe as a csv file
    DF.to_csv("authorListTrimmed.csv", header=False, index=False)

    print("Step 10:", time.strftime("%H:%M:%S", time.localtime()))
    data = json_graph.node_link_data(S)
    s1 = json.dumps(data)
    with open('RV.json', 'w', encoding='utf-8') as f:
        f.write(s1)

    print("Step 11:", time.strftime("%H:%M:%S", time.localtime()))

    # Return graph to call function
    return S, authListTrim, appN