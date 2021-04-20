from sentimentAnalysis import sentiment
from fileNames import files
from TNA import TNAfunc
from FGA import FGAfunc
from nameInput import nameInputFunc, newDataFunc, newName
from authorRank import authorRankFunc
from topRec import topRecFunc, topRecListFunc, topRecFullFunc, authorNegativeSentimentTest, authorListCurrent
from negativeSentimentAnalysis import fullCount, positiveSentiment, printNegativeAnalysis, negativeAnalysis


# A program to produce sentiment analysis output data on Google Play Store reviews using VADER Sentiment Analysis
def main():

    mainPath = "/Users/alexa/Grad/Term1/6414_EECS/Project/Data/datasets-master/sentiment"

    #topRecFullFunc()

    v1 = fullCount()
    print("Val 1:", v1)
    vTemp = v1.copy()
    names = files(mainPath)
    v2 = positiveSentiment(mainPath, names, vTemp)
    print("Val 2:",v1)
    print("Val 3:", vTemp)
    v3 = negativeAnalysis(v1, v2)

    printNegativeAnalysis(v1, v2, v3)

    if newDataFunc():
        names = files(mainPath)
        TNAfunc(mainPath, names)
        authorRankFunc()
    elif newName():
        authorName = nameInputFunc()
        authRecList = topRecFunc(authorName)
        topRecListFunc(authorName, authRecList)

    authorNegativeSentimentTest(authorListCurrent())

    # Give main path name for data
    #mainPath = 'Data/Cleaned_reviews_set_2'

    # Call file name function to get all file names and pathways
    #readFile = files(mainPath)

    # Create statistic file
    #statisticFile = open('Data/sentiment_statistics.csv', 'w', encoding='utf8')

    # Add columns
    #statisticFile.write('App,App ID,Reviews,neg,neu,pos,compound\n')


    # Call sentiment function to get csv output files for all of the applications with English reviews
    #for i in range(len(readFile[0])):
        #sentiment(readFile[0][i], readFile[1][i], statisticFile)

    print("\nThank you for trying our program!")

# Run Main
if __name__ == "__main__":
    main()