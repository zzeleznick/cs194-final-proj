##############
##  HEADER  ##
##############
# AUTHOR: Ollie O'Donnel & Zach Zeleznick
# DATE: December 2015
# COURSE: CS 194-26
# PROJECT: Video Supercuts
# FUNCTION: The main program

############
##  INFO  ##
############
#  Summary:    Dynamically creates a supercut from a video and subtitle pairing
#              where the keyword(s) of interest are spoken

# usage: main.py [-h] [-v] [-p | -w | -s] [videoName] [keywords]

# positional arguments:
#   videoName   The name of the video to process
#   keywords    The words to find in the video

# optional arguments:
#   -h, --help     show this help message and exit
#   -v, --verbose  Displays the phrases that contain the keyword(s) if True
#   -p, --phrase   Captures the entire phrase
#   -w, --word     Refines the bounds to include just the word
#   -s, --speech   Creates a fake speech from the keywords

#############
##  NOTES  ##
#############
# 1. Requires the input video and subtitles to be aligned properly
# 2. config.py sets the input and output folders
# 3. Short words like "we" will have a looser bound for extraction
# 4. If the audio has many pauses or applauses, the bounds are less precise

from config import INPUT_FOLDER, OUTPUT_FOLDER, LOG_FILE, TIMESTAMP_SET
from utils import parseSRT, flatten, testUserInput, listVideoFiles
from moviepy.editor import VideoFileClip, concatenate
import re
import os
import datetime
import argparse
import sys

# ----------==== Step 0 ====---------- #
# ==== Parse Command Line Options ==== #

def parse_cmd_options():
    parser = argparse.ArgumentParser(
        description="Dynamically creates a supercut from a video and subtitle pairing\nwhere the keyword(s) of interest are spoken",
        usage = "%(prog)s [-h] [-v] [-p | -w | -s] [videoName] [keywords]",
        formatter_class= argparse.RawDescriptionHelpFormatter,
        epilog= listVideoFiles() )

    parser.add_argument("filename",  metavar= 'video', nargs='?', default = None,
                        help='The video to process')
    parser.add_argument("keywords", nargs='+', default = ['the'],
                        help='The words to find in the video')
    parser.add_argument("-v", "--verbose", action="store_true",
                        required = False, default = False,
                        help='Displays the phrases that contain the keyword(s) if True')

    group = parser.add_mutually_exclusive_group()

    group.add_argument("-p", "--phrase", action="store_true",
                        required = False, default = False,
                        help='Captures the entire phrase')
    group.add_argument("-w", "--word", action="store_true",
                        required = False, default = False,
                        help='Refines the bounds to include just the word')
    group.add_argument("-s", "--speech", action="store_true",
                        required = False, default = False,
                        help='Creates a fake speech from the keywords')

    args = parser.parse_args()
    print args

    global VERBOSE
    global WORDS
    global MODE_NAME

    videoName = args.filename
    WORDS  = args.keywords
    options = [args.phrase, args.word, args.speech]

    # Check if input arguments are valid #
    valid = testUserInput(videoName)
    if not valid:
        print 'Try a video file from the list [%s] ' % listVideoFiles()
        exit()
    # End input validation #

    # Handling Options #
    VERBOSE = args.verbose

    if True in options:
        MODE = options.index(True)
    else:
        MODE = 0

    optionNames = ['phrases', 'words', 'speech']
    MODE_NAME = optionNames[MODE]

    print "Finding the words: %s\nVideo Name: %s\nOption: %s" % (WORDS, videoName, MODE_NAME)
    # End Handling Options #

    return videoName, WORDS, MODE_NAME

# ----------==== Step 1 ====---------- #
# -==== Load Video and Subtitles ====- #

def loadVideo(fname):
    """
    Probably an array of images + audio, right?
    We'll have to investigate.
    """
    return VideoFileClip(INPUT_FOLDER + fname + ".mp4")

def loadSubs(fname):
    """
    Returns an instance of the Subtitle Class
    """
    return parseSRT(fname)

# ----------==== Step 2 ====---------- #
# -==== Extract Words Occurrences ==== #

def refineBounds(word, line, timeTuple, padding = .10):
    # timeTuple = ("00:00:56,489", "00:00:59,592")
    timeRanges = []
    # Find all occurrences of word in subtitle line
    subLine = " " + " ".join([w.upper() for w in line]) + " "  # no fuzzy matches by adding spaces
    word = " " + str(word) + " "
    # Credit to http://stackoverflow.com/questions/4664850/find-all-occurrences-of-a-substring-in-python
    occurrences = [(m.start(),m.end()) for m in re.finditer(word.upper(), subLine)][:1]
    start, end = timeTuple
    base = datetime.datetime.strptime('00:00:00,000', "%H:%M:%S,%f")
    epoch = datetime.datetime.fromtimestamp(0)
    timeadjust = (epoch - base).total_seconds()
    st, ed = [ datetime.datetime.strptime(var, "%H:%M:%S,%f") for var in [start, end] ]
    st, ed = [(dt - base).total_seconds() for dt in [st, ed]]
    duration = ed - st
    if occurrences and VERBOSE:
        print 'Examining Line: %s' % (line)
        print 'Base timeRange: %s-%s' % (start, end)
    for m_start, m_end in occurrences:
        offset =  float(m_start)/len(subLine)
        padding *= (1 + 4.0 / duration**2)
        if offset < .5:
            true_start = st + offset * duration  - padding * 2 * ( .5 + offset)
            true_end = st + float(m_end)/len(subLine) * duration + padding
        else:
            true_start = ed - (1 - offset) * duration  - padding * 4 * ( .5 + offset )
            true_end = ed - (1 - (float(m_end)/len(subLine)) ) * duration + padding
        ts, te = [ datetime.datetime.fromtimestamp(val - timeadjust) for val in [true_start, true_end] ]
        ts, te = [ str(dt).split()[1][:-3] for dt in [ts, te]]
        if VERBOSE:
            print 'Extracted Times: %s - %s' % (ts, te)
        timeRanges.append([ts, te])
    return timeRanges

def wordOccurrences(subs, words, singleWords=False):
    """
    subs is a dictionary with keys of integers (0, N)
    subs.data[0] --> {"timestamp": timestamp, "text": text}
    subs.words[0] --> ['word1', 'word2']
    subs.times[0] --> ['00:00:00 --> 00:00:04']

    Returns an array of tuples denoting
    the time-ranges when WORD occurs.

    We search for WORD in WORDS:
    - Not Case-Sensitive.
    - Only exact matches of the word
      - (i.e. "african" should not be found for the word "africa").

    For example:
        [("00:01:05","00:01:11"),("00:01:28","00:01:37")]
    """
    segmentedWordList = subs.words
    times = subs.times
    occurrences = []
    if VERBOSE:
        print 'Keywords: %s' % words
    for idx, wordList in enumerate(segmentedWordList):
        for word in words:
            if word.upper() in map(str.upper,wordList):
                if singleWords:  # User chooses to have tight bounds around each word
                    timeRanges = refineBounds(word, wordList, times[idx])
                else:
                    timeRanges = [times[idx]]
                occurrences += timeRanges
                # You only add whole line once
                if not singleWords:
                    break
    if len(occurrences) == 0:
        print "\nThe word(s) "+str(words)+" were not in the video. No supercut could be made.\n"
        sys.exit()
    return occurrences


# ----------==== Step 3 ====---------- #
# -==== Slice Video By Word Cuts ====- #

def slice_video(video,timeRanges):
    """
    We use Zulko's excellent moviepy, and a line from
    http://zulko.github.io/blog/2014/06/21/some-more-videogreping-with-python/
    """
    return concatenate([video.subclip(start, end)
                         for (start,end) in timeRanges])

# ----------==== Step 4 ====---------- #
# ==== Save Video to OUTPUT_FOLDER ==== #

def save_video(fname,video):
    """
    Save the video to OUTPUT_FOLDER + fname + '-' + MODE_NAME + keywords
    """
    if type(WORDS) == list:
        keywordString = '-' + '-'.join([w.upper() for w in WORDS  ])
    else:
        keywordString = '-%s' % WORDS.upper()

    pathname = OUTPUT_FOLDER + fname + '-' + MODE_NAME + keywordString
    video.write_videofile( pathname + ".mp4", fps=video.fps,
                  codec='libx264', audio_codec='aac',
                  temp_audiofile= 'output/temp-audio.m4a',
                  remove_temp=True, audio_bitrate="1000k", bitrate="4000k")

# ----------==== Main ====---------- #
# ----==== Run the Pipeline ====---- #

#   -p, --phrase   Captures the entire phrase
#   -w, --word     Refines the bounds to include just the word
#   -s, --speech   Creates a fake speech from the keywords

def main():
    # STEP 0: Parse Options Based on User Function Choice
    name, words, modeName = parse_cmd_options()
    singleWords = (modeName == "speech" or modeName == "words") # tight bounds around words if True
    fakeSpeech = (modeName == "speech")
    # STEP 1: Load files
    video = loadVideo(name)
    subs = loadSubs(name)
    # STEP 2: Process Subs Into Array
    if fakeSpeech:
        word_occurrences = []
        for word in words:
            first_occurrence = wordOccurrences(subs, [word], singleWords=singleWords)[0]
            print first_occurrence
            word_occurrences.append(first_occurrence)
    else:
        word_occurrences = wordOccurrences(subs, words, singleWords=singleWords)
    if VERBOSE:
        print word_occurrences
    # STEP 3: Slice the Video
    video = slice_video(video, word_occurrences)
    # STEP 4: Save the Video that has been cut.
    save_video(name,video)


def test3():
    subLine = "But it is clear that the two of them had gone down the".split(" ")
    timeRange = ["00:00:56,489","00:00:59,592"]
    word = "the"
    print refineBounds(word, subLine, timeRange)

if __name__ == '__main__':
    main()




