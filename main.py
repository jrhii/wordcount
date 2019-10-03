# Author: Alex Grupas

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

    return wordsAndNums


inFile = "test1.txt"

words = parseFile(inFile)
print(type(words))
print(words)
print(len(words))