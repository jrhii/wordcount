def processWordList(wordList):
    uniqueWords = {word:0 for word in set(wordList)}

    for word in wordList:
        uniqueWords[word] = uniqueWords + 1

    return uniqueWords