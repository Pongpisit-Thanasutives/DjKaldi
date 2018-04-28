import operator
import pandas as pd
import os

dicOfWords = {}

for eachCsvFileName in os.listdir("tables"): 
    if eachCsvFileName.endswith(".csv"):
        df = pd.read_csv("tables/" + eachCsvFileName)
        df = df.iloc[:, 1:]
    
        for word in eachCsvFileName.replace('.csv', '').split(' '):
            if word.lower() not in dicOfWords:
                dicOfWords[word.lower()] = [0,0]
                dicOfWords[word.lower()][0] += len(df[df[word]==1])
                dicOfWords[word.lower()][1] += 9
            else:
                if word + '.1' in df:
                    dicOfWords[word.lower()][0] += len(df[df[word+'.1']==1])
                    dicOfWords[word.lower()][1] += 9
        
        likelyToBeCorrectlyTranscricedWords = []
        likelyToBeMistranscricedWords = []
        
        for eachColumn in df:
            if int(df[eachColumn].mode()) == 1:
                likelyToBeCorrectlyTranscricedWords.append(eachColumn.lower())
            else:
                likelyToBeMistranscricedWords.append(eachColumn.lower())
        
        print("Words transcribed most correctly : ", likelyToBeCorrectlyTranscricedWords)
        print("Words transcribed most incorrectly : ", likelyToBeMistranscricedWords)
        print("-----")

i = 1
# print(dicOfWords)
# print(sorted(dicOfWords.items(), key=lambda x : x[1][0] / x[1][1]))

for (w, l) in sorted(dicOfWords.items(), key=lambda x : x[1][0] / x[1][1]):
    c = l[0]; t = l[1]
    print(str(i), w, "-->", c, "correct transcribed out of", t)
    i += 1