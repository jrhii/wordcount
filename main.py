# Authors: Alex Grupas, James Harter, Ian Green

import re
import sys
import pygame
import time


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
    return wordDict


# Function: sortWordsByAlpha
# Use: To be passed to `list.sort()` as key
def sortWordsByAlpha(wordDict):
    return wordDict["word"]


def getLongestWord(wordList):
    maxWordLen = 1
    for word in wordList:
        if len(word) > maxWordLen:
            maxWordLen = len(word)
    return maxWordLen

#Graphical output
def drawGraph(words, dicts):

    clock = pygame.time.Clock()  # manages screen update and animation speed
    grey = (100, 100, 100)  # grid color
    black = (0, 0, 0)
    orange = (255, 140, 0)
    purple = (180, 0, 255)
    yellow = (255, 255, 0)

    barWidth = 7 * getLongestWord(words)  # size of each cell
    barHeight = 15

    pygame.init()  # start pygame for generating visual output
    pygame.display.set_caption("Dictionary Graph")  # set window title
    font = pygame.font.Font(pygame.font.get_default_font(), 12)
    windowX =22 * barWidth
    windowY = len(dicts) * barHeight
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
                posYbot = barHeight

                for r in range(len(dicts) + 2):  # draw graph lines
                    pygame.draw.line(gameDisplay, grey, (r * barWidth, 0), (r * barWidth, len(dicts) * barWidth), 1)
                pygame.draw.rect(gameDisplay, purple, (posX, windowY - 3*posYbot, barWidth, -posYtop))  # draw word bar
                pygame.draw.line(gameDisplay, orange, (posX, windowY - 3*posYbot), (posX + barWidth, windowY - 3*posYbot), 2)  # draw y axis
                pygame.draw.line(gameDisplay, orange, (barWidth, windowY - 3*posYbot), (barWidth, 0), 3)  # draw x axis
                pygame.draw.line(gameDisplay, yellow, (barWidth, windowY - 3*posYbot - posYtop - 1), (posX + barWidth, windowY - 3*posYbot - posYtop - 1), 1)  # draw top of bar indicator line

                wordLabel = font.render(word, False, orange)
                countlabel = font.render(str(itr), False, orange)
                gameDisplay.blit(wordLabel, (posX + 2, windowY - 2*posYbot))  # draw x axis labels
                gameDisplay.blit(countlabel, (barWidth-20, windowY - (itr * barHeight) - 3 * barHeight))  # draw y axis labels

                pygame.event.pump()
                pygame.display.update()  # update screen
                clock.tick(30)  # variable display speed control based on size of the grid.
    input()  # wait to kill graph
    pygame.quit()

inFile = "test1.txt"

words = parseFile(inFile)
print(type(words))
print(words)
print(len(words))

wordDicts = processWordList(words)
print(wordDicts)

cleanDict = processCleanWordList(words)  # remove display strings
cleanDict = sortWordsByCount(cleanDict)  # sort to highest 20 get graphed
drawGraph(words, cleanDict)  # graph it

#I noticed that it seems to have some issue with EOF. if there is no return line after the last word it fails to count
# the last word. probably due to how that extra space was being handled.
# Graph scales really weird with truly gigantic words
# count sort needs finished. until then it just cuts off whatever happens to be past word 20 in the list