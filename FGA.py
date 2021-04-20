from networkx.algorithms import bipartite

from pylab import *
import networkx as nx
import pandas as pd
import matplotlib.lines as lines
from operator import itemgetter
from fileNames import files
from TNA import TNAfunc
import multiprocessing
import time

def FGAfunc():

    t = time.localtime()
    ct = time.strftime("%H:%M:%S", t)

    print("Start", ct)

    # Open input csv file, and create output files
    dataset = pd.read_csv('frequencyTest.csv', delimiter=',')
    appNames = pd.read_csv('apps_names.csv', delimiter=',')
    topologyStatisticsFile = open("topologyStatistics.txt", 'w', encoding='utf8')
    graphDictionaryFile = open("graphDictionary.txt", 'w', encoding='utf8')
    #T = nx.read_gpickle("G_APP.gpickle")
    #print("Test!")
    Y = nx.read_gpickle("G_COMPLETE.gpickle")
    #mainPath="/Users/alexa/Grad/Term1/6414_EECS/Project/Data/datasets-master/sentiment"
    #names = files(mainPath)
    #Y = TNAfunc(mainPath, names)
    #print(nx.info(Y))
    #####################################################appList = []

    # Find list of all apps commented on #####################################################
    #####################################################for i in range(dataset['App'].count()):
        #####################################################splitVal = dataset['App'][i].split(';')
        #####################################################for j in range(len(splitVal)):
            #####################################################appList.append(splitVal[j])

    # Remove redundant entries, and put into a dictionary with a base comment score of 0 #####################################################
    #####################################################appList = set(appList)
    #####################################################appList = list(appList)
    #####################################################appList = {i: 0 for i in appList}
    authList = {}

    # Create dictionary for author values. Including name, apps commented on, and number of apps commented on
    for i in range(dataset['Author'].count()):
        aVal1 = dataset['Author'][i]
        aVal2 = dataset['App'][i]
        aVal3 = dataset['Total'][i]
        authList[aVal1] = aVal2, aVal3

    # Create and name graph #####################################################
    #####################################################G = nx.Graph()
    H = nx.Graph()
    H.name = "Topological Network Analysis"

    # Add author list and apps list #####################################################
    #H.add_nodes_from(authList.keys())
    #####################################################G.add_nodes_from(appList.keys(), bipartite=0)
    #####################################################G.add_nodes_from(authList.keys(), bipartite=1)

    # Add edge between every author and every app they commented on #####################################################
    #####################################################for key, value in authList.items():
        #####################################################for k, v in appList.items():
            #####################################################if k in authList[key][0]:
                #####################################################G.add_edge(key, k, weight=0.25)
                #####################################################appList[k] += 1

    #o = list(G.edges)

    #print("YO", Y.edges.values())
    #print("YO", appNames.values)

    W = nx.Graph()

    val4=[]

    #listY = enumerate(Y)

    #####################################################nal = []

    # Add nodes to H based on binary sentiment output
    for u in Y:
        nodeAdded = False
        #print("No way", u)
        for j in appNames.values:
            if nodeAdded == True:
                break
            if u in appNames.values:
                #print("No way", u)
                break
            #print(j[0])
            #print(u)
            if Y.has_edge(j[0], u):
                #print("YOOOOOOOOOOOOOO")
                val8=0
                #print(u)
                currentWeight = Y[u][j[0]]['weight']
                #####################################################nal.append(u)
                if 'b' == Y[u][j[0]]['color']:
                    #print("B---------------",u)
                    H.add_node(u)
                    #W.add_edge(j[0], u, weight=currentWeight)
                    nodeAdded = True
                elif 'k' == Y[u][j[0]]['color']:
                    #print("K---------------",u)
                    H.add_node(u)
                    #W.add_edge(j[0], u, weight=currentWeight)
                    nodeAdded = True

    # Creates new trimmed Y with W, based on binary sentiment output
    for i, j in Y.edges:
        #print("THIS IS:", i, j)
        #if i in appNames.values:
            #print("No way", i)
            #continue
        #if j in appNames.values:
            #print("No way", j)
            #continue
        currentWeight = Y[i][j]['weight']
        #####################################################nal.append(u)
        if 'b' == Y[i][j]['color']:
            # print("B---------------", u)
            # H.add_node(u)
            W.add_edge(i, j, weight=currentWeight)
            # nodeAdded = True
        elif 'k' == Y[i][j]['color']:
            # print("K---------------", u)
            # H.add_node(u)
            W.add_edge(i, j, weight=currentWeight)
            # nodeAdded = True

    #print(W.edges)

    W.remove_nodes_from(nx.isolates(W))

    #print("This is a weight", Y["A Goldstein"]["Google Photos"]["weight"])
    #print("This is a weight", Y["A Jacks"]["Google Photos"]["weight"]/10000)
    #print("This is a weight", Y["A Krishna"]["Google Photos"]["weight"])
    #print("This is a weight", Y["A L"]["Google Photos"]["weight"])

    #print("This is an edge", Y["A Goldstein"]["Google Photos"])
    #print("This is an edge", Y["A Jacks"]["Google Photos"])
    #print("This is an edge", Y["A Krishna"]["Google Photos"])
    #print("This is an edge", Y["A L"]["Google Photos"])

    ###jc = nx.jaccard_coefficient(G)

    jc = nx.jaccard_coefficient(W)#, authList.keys())

    #print(W)

    #G.remove_edges_from(list(G.edges()))

    #print(G)

    #print(appList.items())
    #print(jc)

    #for u, v, p in jc:
        #for k in appList.items():
            #print(appList[k])
            #if u in appList[k][0]:
                #jc.remove(u)

    #print(appList)
    #H.remove_edges_from(appList)

    widthVal = []

    jcl = list(jc)

    #print(jcl)

    #print("List 1:",jcl)

    jcln = []

    print("Step 2:", time.strftime("%H:%M:%S", time.localtime()))

    for u, v, p in jcl:
        #print("Here in app remove 1",jcl.index(u))
        sp = float(p)

        if sp > 0.0 and u not in appNames.values and v not in appNames.values:
            #print("Here in app append 1", u, v, p)
            jcln.append((u, v, p))
            #jcl.pop(jcl.index(u))
        #elif v not in appNames.values:
            #print("Here in app remove 2", u, v, p)
            #jcl.add((u, v, p))

    #print("List 2:", jcln,"!!!!!!!!!!!!!!!!DUDe uughhhhh")

    print("Step 3:", time.strftime("%H:%M:%S", time.localtime()))

    for u, v, p in jcln:

        ###Uncomment to add width###
        #widthVal.append(float(p))

        #print(u, v, p)
        sp = float(p)
        #print("Here")
        #if sp > 0.0 and u not in appNames.values and v not in appNames.values:
            #print(sp)
            #print("yes!!!!!!!!!!!!!!!!")
        H.add_edge(u, v, weight=sp)
            #print("Here in the loop")

    #print(H.edges)

    hEdgeCount = {}

    print("Step 4:", time.strftime("%H:%M:%S", time.localtime()))

    #####################################################
    #for f in H.nodes:
        #hEdgeCount[f] = len(H.edges(f))
        #print("Here in the second loop")
    #####################################################

    #print(hEdgeCount)

    #H.remove_edges_from(appList)

    #for k in knn:
        #if k in authList[key][0]:
            #G.add_edge(key, k, weight=0.25)
            #appList[k] += 1

    #print(o)

    #print(H.edges(appList[0]))

    #for y, g in appList.items():
        #H.remove_edge(H.edges(appList.keys()))

    #H.remove_nodes_from(appNames.values)

    #print(G.edges)

    #####################################################
    # Print statistical information
    #print(nx.info(H))
    topologyStatisticsFile.write(str(nx.info(H))+"\n")
    density = nx.density(H)
    #print("Network density:", density)
    topologyStatisticsFile.write("Network density: "+str(density))
    degree_dict = dict(H.degree(H.nodes()))
    nx.set_node_attributes(H, degree_dict, 'degree')
    #sorted_degree = sorted(degree_dict.items(), key=itemgetter(1), reverse=True)
    #print("Top 5 nodes by degree:")
    #for d in sorted_degree[:5]:
        #print(d)
    #####################################################

    # Determine node size
    #appWeight = [float(l)*50 for x,l in appList.items()]
    #authWeight = [l for x,l in authList.items()]
    #print(authList.items())
    #####################################################authWeight = [float(l)*20 for x, l in hEdgeCount.items()]
    #print(authWeight)

    #print(H.edges)

    # Map to layout #####################################################
    #pos = nx.spring_layout(H, k=0.25, iterations=70, scale=10)
    #print(H.size())
    #plt.figure(1, figsize=(100,100))
    #####################################################


    #print("yo = "+str(size(authList.keys())))
    #print(size(authWeight))

    # Draw network #####################################################
    #nx.draw_networkx_nodes(H, pos=pos, node_color="red", nodelist=appList.keys(), node_size=appWeight)
    #nx.draw_networkx_nodes(H, pos=pos, node_color="blue", nodelist=H.nodes, node_size=authWeight)
    #nx.draw_networkx_edges(H, pos=pos)###Uncomment to add width###, width=widthVal)
    #####################################################

    # Add legend
    #p = mlines.Line2D([],[],label="Author",color="blue")
    #a = mlines.Line2D([],[],label="Application",color="red")
    #plt.legend(handles=[p,a])

    #print(multiprocessing.cpu_count())
    # Print graph list to output, and output image
    graphDictionaryFile.write(str(H.edges))
    #####################################################plt.savefig("FoldedGraphAnalysis.jpg")

    print("Step 5:", time.strftime("%H:%M:%S", time.localtime()))

    # Return graph to call function
    return H