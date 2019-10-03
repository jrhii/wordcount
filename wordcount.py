#Takes a list of strings, outputs a list of dictionaries in the following form:
#   [{"word": <String>, "count": <Number>}]
def processWordList(wordList):

    uniqueWordsDict = {word:0 for word in set(wordList)}

    for word in wordList:
        uniqueWordsDict[word] = uniqueWordsDict[word] + 1

    uniqueWordsList = []
    for word, count in uniqueWordsDict.items():
        uniqueWordsList.append({"word": word, "count": count})
    
    return uniqueWordsList

#To be passed to `list.sort()` as key
def sortWordsByCount(wordDict):
    return wordDict["count"]

#To be passed to `list.sort()` as key
def sortWordsByAlpha(wordDict):
    return wordDict["word"]