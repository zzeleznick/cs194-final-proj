##############
##  HEADER  ##
##############
# AUTHOR: Ollie O'Donnel & Zach Zeleznick
# DATE: December 2015
# COURSE: CS 194-26
# PROJECT: Video Supercuts
# FUNCTION: General Utilties

import re
import os, sys
import time
from itertools import chain
# internals
from config import INPUT_FOLDER, OUTPUT_FOLDER, LOG_FILE, TIMESTAMP_SET
from classes import SubtitleClass
from classes import WordTokenizer as wdtk


def zprint(*stream):
    '''
    Prints messages to a log file as specified in LOG_FILE variable
    '''
    with open(LOG_FILE, 'a') as myLog:
        global TIMESTAMP_SET
        if not TIMESTAMP_SET:
            myLog.writelines('\n' + str(sys.argv[0]) + ' run at ' + time.strftime("%Y-%m-%d %H:%M") + '\n')
            TIMESTAMP_SET = True
        for arg in stream:
            myLog.writelines(str(arg) + ' ')  # safe cast to string and add trailing space
        myLog.writelines('\n')  # end with newline

def flatten(listOfLists):
    "Flatten one level of nesting"
    return chain.from_iterable(listOfLists)


def listVideoFiles():
    pureNumbers = re.compile(r'^[0-9]*$')
    fileNames = [f[:f.index('.mp4')] for f in os.listdir(INPUT_FOLDER) if f.endswith('.mp4')]
    fileNames = [ f for f in fileNames if pureNumbers.match(f)]
    return 'Video Files: ' + ' | '.join(fileNames)


def listOutputVideoFiles():
    folders = [f for f in os.listdir(OUTPUT_FOLDER) if os.path.isdir(OUTPUT_FOLDER+f)]
    fileNames = []
    for folder in folders:
        names = []
        for f in os.listdir(OUTPUT_FOLDER+folder):
            if f.endswith('.mp4'):
                names.append(f[:f.index('.mp4')])
        fileNames.append(str(folder) + ': ' + ", ".join(names))
    return str(fileNames)


def parseSRT(fname):
    lines = []
    ext = '.srt'
    if fname.endswith(ext):
        fname = fname[0:fname.index(ext)]
    with open(INPUT_FOLDER + fname + ext, 'r') as infile:
        lines = infile.readlines()[4:-1]
    # NOTE: lines [0:4] always are always junk, and last 2 are blank
    # NOTE: Can contain odd span text
    '''
    1 # id
    0:00:00 --> 0:00:04  # timestamp
    &gt;&gt; Let&#39;s say you&#39;re a college freshman and you&#39;re choosing a major. You&#39;re # text
    \n # blank
    '''
    # Starting with 0, want to collect lines 1,2 and then 5,6 since 3 is blank, 4 is #id which we discard
    # parsed = [ lines[i:i+2] for i in range(1, len(lines), 4) ]
    # WARNING THE PRIOR LINE IS NOT DYNAMIC ENOUGH
    lineStarters = []
    pureNumbers = re.compile(r'^[0-9]*$')
    for idx, line in enumerate(lines):
        line = line.strip().replace('\n', '') # empty matches can occur
        if line and pureNumbers.match(line):
            lineStarters.append(idx)

    parsed = []

    for i in range(len(lineStarters)- 1):
        stamp = lines[lineStarters[i]+1] # skip the index and take the timestamp
        text = ''.join(lines[lineStarters[i]+2: lineStarters[i+1] - 1]) # skip the final blank
        parsed.append([stamp, text])

    lastStamp = lines[lineStarters[-1]+1] # skip the index and take the timestamp
    lastText = ''.join(lines[lineStarters[-1]+2:]) # skip the final blank
    parsed.append([lastStamp, lastText])

    dataDict = {}
    with open(OUTPUT_FOLDER + fname + '.txt', 'w') as outfile:
        for idx, line in enumerate(parsed):
            timestamp, text = line
            timestamp = timestamp.strip()
            timestamp = timestamp.split(" ")
            timestamp.pop(1)
            translations = [ ['&#39;', "'"], # apostrophe
                             ['&gt;', ">"], # greater than sign
                            ]
            # Let's replace this with a library if we have time. There are many more escaped characters than these two.
            for original, translated in translations:
                text = text.replace(original, translated)  # translate junk
            dataDict[idx] = {"timestamp": timestamp, "text": text}
            outfile.writelines(str(timestamp)+ '\n' + text + '\n')
    Subtitles = SubtitleClass(fname, dataDict)
    '''
    print(Subtitles)
    print 'Total Number of words: %d | Uniques: %d' % (Subtitles.wordCount, Subtitles.uniqueWordCount() )
    fd = Subtitles.freqDist
    for word in fd.keys():
        print word, fd[word]
    print Subtitles.words
    print Subtitles.times
    '''
    return Subtitles

if __name__ == '__main__':
    parseSRT('Intro')