import networkx as nx
import pandas as pd
import time

# This function folds the original bipartite network into an author only network
def FGAfunc():

    t = time.localtime()
    ct = time.strftime("%H:%M:%S", t)

    print("Start", ct)

    # Open input csv file, and create output files
    dataset = pd.read_csv('frequencyTest.csv', delimiter=',')
    appNames = pd.read_csv('apps_names.csv', delimiter=',')
    topologyStatisticsFile = open("topologyStatistics.txt", 'w', encoding='utf8')
    graphDictionaryFile = open("graphDictionary.txt", 'w', encoding='utf8')
    Y = nx.read_gpickle("G_COMPLETE.gpickle")
    authList = {}

    # Create dictionary for author values. Including name, apps commented on, and number of apps commented on
    for i in range(dataset['Author'].count()):
        aVal1 = dataset['Author'][i]
        aVal2 = dataset['App'][i]
        aVal3 = dataset['Total'][i]
        authList[aVal1] = aVal2, aVal3

    # Create and name graph #####################################################
    H = nx.Graph()
    H.name = "Topological Network Analysis"

    W = nx.Graph()

    val4=[]

    # Add nodes to H based on binary sentiment output
    for u in Y:
        nodeAdded = False
        for j in appNames.values:
            if nodeAdded == True:
                break
            if u in appNames.values:
                break
            if Y.has_edge(j[0], u):
                val8=0
                currentWeight = Y[u][j[0]]['weight']
                #####################################################nal.append(u)
                if 'b' == Y[u][j[0]]['color']:
                    H.add_node(u)
                    nodeAdded = True
                elif 'k' == Y[u][j[0]]['color']:
                    H.add_node(u)
                    nodeAdded = True

    # Creates new trimmed Y with W, based on binary sentiment output
    for i, j in Y.edges:
        currentWeight = Y[i][j]['weight']
        if 'b' == Y[i][j]['color']:
            W.add_edge(i, j, weight=currentWeight)
        elif 'k' == Y[i][j]['color']:
            W.add_edge(i, j, weight=currentWeight)

    W.remove_nodes_from(nx.isolates(W))

    jc = nx.jaccard_coefficient(W)

    widthVal = []

    jcl = list(jc)

    jcln = []

    print("Step 2:", time.strftime("%H:%M:%S", time.localtime()))

    for u, v, p in jcl:
        sp = float(p)

        if sp > 0.0 and u not in appNames.values and v not in appNames.values:
            jcln.append((u, v, p))

    print("Step 3:", time.strftime("%H:%M:%S", time.localtime()))

    for u, v, p in jcln:

        sp = float(p)
        H.add_edge(u, v, weight=sp)

    hEdgeCount = {}

    print("Step 4:", time.strftime("%H:%M:%S", time.localtime()))

    #####################################################
    #for f in H.nodes:
    #   hEdgeCount[f] = len(H.edges(f))
    #   print("Here in the second loop")
    #####################################################

    # Print statistical information
    print(nx.info(H))
    topologyStatisticsFile.write(str(nx.info(H))+"\n")
    density = nx.density(H)
    topologyStatisticsFile.write("Network density: "+str(density))
    degree_dict = dict(H.degree(H.nodes()))
    nx.set_node_attributes(H, degree_dict, 'degree')

    # Determine node size #####################################################
    #authWeight = [float(l)*20 for x, l in hEdgeCount.items()]
    #####################################################

    # Map to layout #####################################################
    #pos = nx.spring_layout(H, k=0.25, iterations=70, scale=10)
    #print(H.size())
    #plt.figure(1, figsize=(100,100))
    #####################################################

    # Draw network #####################################################
    #nx.draw_networkx_nodes(H, pos=pos, node_color="red", nodelist=appList.keys(), node_size=appWeight)
    #nx.draw_networkx_nodes(H, pos=pos, node_color="blue", nodelist=H.nodes, node_size=authWeight)
    #nx.draw_networkx_edges(H, pos=pos)###Uncomment to add width###, width=widthVal)
    #####################################################

    # Print graph list to output, and output image
    graphDictionaryFile.write(str(H.edges))

    print("Step 5:", time.strftime("%H:%M:%S", time.localtime()))

    # Return graph to call function
    return H