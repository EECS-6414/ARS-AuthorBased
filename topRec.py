import networkx as nx
import pandas as pd
import json

def authorListCurrent():
    authList = pd.read_csv('authorListTrimmed.csv', delimiter=',')
    authL = []
    for j in authList.values:
        if j[0] in authList.values and j != "App":
            authL.append(j[0])
    return authL

def authorNegativeSentimentTest(authL):
    authList = pd.read_csv('negativeSentimentTest.csv', delimiter=',')
    authNegative = []
    count = 0
    for j in authList.values:
        if j[0] in authList.values and j != "App":
            authNegative.append(j[0])
    for i in authNegative:
        if i in authL:
            count += 1
    total = len(authL)
    difference = count/total
    percentage = round(difference * 100, 2)
    print("\nPercent of users who:")
    print("\t- reviewed at least 5 apps\n\t- had at least 1 positive review\n\n\t",percentage,"%")

def topRecFunc(name):
    roundedValue = 2
    S = nx.read_gpickle("S_COMPLETE.gpickle")
    appList = pd.read_csv('apps_names.csv', delimiter=',')
    appL = []
    for j in appList.values:
        if j[0] in appList.values and j != "App":
            appL.append(j[0])

    recList = {}
    recListOrdered = {}

    if name in S.nodes:
        for i in S[name]:
            recList[i] = round(S[name][i]["weight"], roundedValue)

        recKeyOrdered = sorted(recList, key=recList.get, reverse=True)

        for i in recKeyOrdered:
            recListOrdered[i] = recList[i]

        authorDict = {name: recListOrdered}
        authorJson = json.dumps(authorDict)
        with open('currentAuthor.json', 'w', encoding='utf-8') as f:
            f.write(authorJson)

        return recListOrdered

    else:
        return {}

def topRecListFunc(name, authorList):
    if len(authorList) > 0:

        print("\nHere are the top 5 recommendations (or less) for", name)
        count = 0
        max = 5
        for i in authorList:
            count += 1
            print(count, "-", i)
            print("\tScore: ", authorList[i])
            if count == max:
                break

    else:

        print("\nNo recommendation available for this author.")

def topRecFullFunc():
    authorListFullDict = {}
    authList = authorListCurrent()
    for i in authList:
        authorListFullDict[i] = topRecFunc(i)
        print(i)

    authorListFullJson = json.dumps(authorListFullDict)
    with open('authorRecListFull.json', 'w', encoding='utf-8') as f:
        f.write(authorListFullJson)