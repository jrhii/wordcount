# Authors: Alex Grupas, James Harter, Ian Green

import re
import sys

# Function: parseFile
# Use: Will take in a filename, open the file, extract all the numbers and words from
# the file and return those numbers and words as a list
def parseFile(filename):
    try:
        f = open(filename, 'r')
        dataFromFile = f.read()
    except FileNotFoundError:
        print("Something went wrong while trying to open the file")
        sys.exit()

    # this step will find all words that are hyphenated on two seperate lines
    dataFromFile = re.sub(r'-\n(\w+ *)', r'\1\n', dataFromFile)

    hyphenatedStep = re.sub("-", "", dataFromFile) # removes hypens from words hyphenated on same line
    apostropheStep = re.sub("'", "", hyphenatedStep) # removes apostrophes
    exclamationStep = re.sub("!", "", apostropheStep) # removes exclamtion points

    wordsAndNums = re.split(r"[\s\.,\?]+", exclamationStep)

    # was getting bug where last item in list was an empty string so I am just deleting it
    del wordsAndNums[-1]

    return wordsAndNums

#Function: processWordList
#Use: Takes a list of strings, outputs a list of dictionaries in the following form:
#   [{"word": <String>, "count": <Number>}]
def processWordList(wordList):

    uniqueWordsDict = {word:0 for word in set(wordList)}

    for word in wordList:
        uniqueWordsDict[word] = uniqueWordsDict[word] + 1

    uniqueWordsList = []
    for word, count in uniqueWordsDict.items():
        uniqueWordsList.append({"word": word, "count": count})
    
    return uniqueWordsList

#Function: sortWordsByCount
#Use: To be passed to `list.sort()` as key
def sortWordsByCount(wordDict):
    return wordDict["count"]

#Function: sortWordsByAlpha
#Use: To be passed to `list.sort()` as key
def sortWordsByAlpha(wordDict):
    return wordDict["word"]


inFile = "test1.txt"

words = parseFile(inFile)
print(type(words))
print(words)
print(len(words))

wordDicts = processWordList(words)
print wordDicts