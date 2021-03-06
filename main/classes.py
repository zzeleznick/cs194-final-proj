##############
##  HEADER  ##
##############
# AUTHOR: Ollie O'Donnel & Zach Zeleznick
# DATE: December 2015
# COURSE: CS 194-26
# PROJECT: Video Supercuts
# FUNCTION: Support Classes

import re

class WordTokenizer:
    """Class for splitting text into words"""
    def __init__(self, text):
        self.text = text

    def tokenize(self, keepPunctuation = False):
            '''
            :param text: a string (sentence)
            :returns: a list of strings (words)
            '''
            text = self.text
            pauses = re.compile(r'[\.,;:!\?]')
            text = pauses.sub(' ' + '~' * 8, text)
            pattern = re.compile(r'[\[\]\(\)\{\}\.,;:!><\?\"\'_`]')
            if keepPunctuation:
                scrubbed = text # TODO: do later
            else:
                scrubbed = pattern.sub('', text)
            split = scrubbed.split()
            return split

class SubtitleClass:
    """Class for handling srt files and returning a dictionary like object"""
    def __init__(self, name, dataDictionary):
        def buildTimeSegments(dataDict):
            # dataDict is generated in utils.py
            times = [ entry['timestamp'] for entry in dataDict.values() ]
            return times

        def buildTimeSegmentedWordList(dataDict):
            textList = [ entry['text'].replace('\n', ' ') for entry in dataDict.values() ]
            words = [ WordTokenizer(text).tokenize() for text in textList ]
            return words

        def buildFreqDist(wordlistList):
            freqDist = {}
            totalWords = 0
            for lst in wordlistList:
                for word in lst:
                    totalWords += 1
                    if word not in freqDist:
                        freqDist[word] = 1
                    else:
                        freqDist[word] += 1
            return freqDist, totalWords

        self.name = name
        self.data = dataDictionary
        self.times = buildTimeSegments(dataDictionary) # array of strings
        self.words = buildTimeSegmentedWordList(dataDictionary) # giant 2d array. Wordlist for each timestamp.
        self.freqDist, self.wordCount = buildFreqDist(self.words)
        self.lineCount = len(self.data.keys())

    def uniqueWordCount(self):
        return len(self.freqDist.keys())

    def __repr__(self):
        return '<SubtitleObj: %s | lines: %d | words: %d>' %  (self.name, self.lineCount, self.wordCount)

    def __str__(self):
        return repr(self)
