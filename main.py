from fileNames import files
from TNA import TNAfunc
from nameInput import nameInputFunc, newDataFunc, newName, newNegativeSentimentAnalysis
from authorRank import authorRankFunc
from topRec import topRecFunc, topRecListFunc, authorNegativeSentimentTest, authorListCurrent
from negativeSentimentAnalysis import fullCount, positiveSentiment, printNegativeAnalysis, negativeAnalysis


# A program to produce sentiment analysis output data on Google Play Store reviews using VADER Sentiment Analysis
def main():

    mainPath = "/Users/alexa/Grad/Term1/6414_EECS/Project/Data/datasets-master/sentiment"

    if newDataFunc():
        names = files(mainPath)
        TNAfunc(mainPath, names)
        authorRankFunc()
    elif newName():
        authorName = nameInputFunc()
        authRecList = topRecFunc(authorName)
        topRecListFunc(authorName, authRecList)
    elif newNegativeSentimentAnalysis():
        v1 = fullCount()
        vTemp = v1.copy()
        names = files(mainPath)
        v2 = positiveSentiment(mainPath, names, vTemp)
        v3 = negativeAnalysis(v1, v2)
        printNegativeAnalysis(v1, v2, v3)
        authorNegativeSentimentTest(authorListCurrent())

    print("\nThank you for trying our program!")

# Run Main
if __name__ == "__main__":
    main()