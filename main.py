# Authors: Alex Grupas, James Harter, Ian Green

import re
import sys
import pygame
import collections


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

    hyphenatedStep = re.sub("-", "", dataFromFile)  # removes hypens from words hyphenated on same line
    apostropheStep = re.sub("'", "", hyphenatedStep)  # removes apostrophes
    exclamationStep = re.sub("!", "", apostropheStep)  # removes exclamtion points

    wordsAndNums = re.split(r"[\s\.,\?]+", exclamationStep)

    # was getting bug where last item in list was an empty string so I am just deleting it
    del wordsAndNums[-1]

    return wordsAndNums


# Function: processWordList
# Use: Takes a list of strings, outputs a list of dictionaries in the following form:
#   [{"word": <String>, "count": <Number>}]
def processWordList(wordList):
    uniqueWordsDict = {word: 0 for word in set(wordList)}

    for word in wordList:
        uniqueWordsDict[word] = uniqueWordsDict[word] + 1

    uniqueWordsList = []
    for word, count in uniqueWordsDict.items():
        uniqueWordsList.append({"word": word, "count": count})

    return uniqueWordsList


def processCleanWordList(wordList):
    uniqueWordsDict = {word: 0 for word in set(wordList)}

    for word in wordList:
        uniqueWordsDict[word] = uniqueWordsDict[word] + 1

    return uniqueWordsDict


# Function: sortWordsByCount
# Use: To be passed to `list.sort()` as key
def sortWordsByCount(wordDict):
    wordDict = collections.OrderedDict(sorted(wordDict.items(), key=lambda x: x[1], reverse=True))
    return wordDict


# Function: sortWordsByAlpha
# Use: To be passed to `list.sort()` as key
def sortWordsByAlpha(wordDict):
    return wordDict["word"]


# Returns length of the longest word used to set min col width
def getLongestWord(wordList):
    maxWordLen = 1
    for word in wordList:
        if len(word) > maxWordLen:
            maxWordLen = len(word)
    return maxWordLen


# Returns maximum number of times any one word occurs
def getMostWord(wordDict):
    maxWord = 1
    for word in wordDict:
        if wordDict[word] > maxWord:
            maxWord = wordDict[word]
    return maxWord


# Graphical output
def drawGraph(words, dicts):

    clock = pygame.time.Clock()  # manages screen update and animation speed
    grey = (75, 75, 75)  # grid color
    black = (0, 0, 0)
    orange = (255, 140, 0)
    purple = (100, 0, 255)

    barWidth = 6 * getLongestWord(words)  # dynamic col width to fit longest word
    barHeight = 15

    pygame.init()  # start pygame for generating visual output
    pygame.display.set_caption("Dictionary Graph")  # set window title
    font = pygame.font.Font(pygame.font.get_default_font(), 12)
    windowX = 22 * barWidth
    windowY = 22 * barHeight
    gameDisplay = pygame.display.set_mode((windowX, windowY))
    gameDisplay.fill(black)  # set background color

    done = False  # game window exited
    while done is False:  # pygame loop
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # exit loop
        itr = 0
        while True:
            for word in dicts:
                if itr is 20:
                    break
                itr = itr + 1
                posX = barWidth * itr  # get x position
                posYtop = dicts[word] * barHeight

                # Draw each shaded word col
                pygame.draw.rect(gameDisplay, purple, (posX, windowY - 3 * barHeight, barWidth, -posYtop))

                # Draw each word label
                wordLabel = font.render(word, False, orange)
                gameDisplay.blit(wordLabel, (posX + 2, windowY - 2*barHeight))  # draw x axis labels

            # Draw grid
            for r in range(22):  # draw vertical graph lines
                pygame.draw.line(gameDisplay, grey, (r * barWidth, 0), (r * barWidth, windowY - 3 * barHeight), 1)
            for r in range(20):  # draw horizontal graph lines
                pygame.draw.line(gameDisplay, grey, (barWidth, windowY - r * barHeight - 3 * barHeight), (21 * barWidth, windowY - r * barHeight - 3 * barHeight), 1)

            # Draw x & y axis
            pygame.draw.line(gameDisplay, orange, (barWidth, windowY - 3 * barHeight), (21 * barWidth, windowY - 3 * barHeight), 2)  # draw x axis
            pygame.draw.line(gameDisplay, orange, (barWidth, windowY - 3 * barHeight), (barWidth, 0), 3)  # draw y axis

            # Draw y axis labels
            for i in range(getMostWord(dicts)):
                countlabel = font.render(str(i + 1), False, orange)
                gameDisplay.blit(countlabel, (barWidth-20, windowY - (( i + 1) * barHeight) - 3 * barHeight))

                # update screen
            pygame.event.pump()
            pygame.display.update()
            clock.tick(30)
            input()  # wait to kill graph
            pygame.quit()


inFile = "test1.txt"

words = parseFile(inFile)
print(type(words))
print(words)
print(len(words))

wordDicts = processWordList(words)
print(wordDicts)

print("\nPress enter to exit graphical output")
cleanDict = processCleanWordList(words)  # remove display strings
cleanDict = sortWordsByCount(cleanDict)  # sort so highest 20 get graphed
drawGraph(words, cleanDict)  # graph it

#I noticed that it seems to have some issue with EOF. if there is no return line after the last word it fails to count
# the last word. probably due to how that extra space was being handled.
# Graph scales really weird with truly gigantic words