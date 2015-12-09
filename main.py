from utils import parseSRT, flatten
from moviepy.editor import VideoFileClip, concatenate
import re
import time

# ---------==== Step 1 ====---------- #

def loadVideo(fname):
    """
    Probably an array of images + audio, right?
    We'll have to investigate.
    """
    return VideoFileClip("data/"+fname+".mp4")

def loadSubs(fname):
    """
    Returns an instance of the Subtitle Class
    """
    return parseSRT(fname)

# ---------==== Step 2 ====---------- #

def refineBounds(word, subLine, timeRange, padding=0.1):
    """
    subLine = "But it is clear that the two of them had gone down the"
    timeRange = (["00:00:56,489"],["00:00:59,592"])
    word = "the"
    """
    timeRanges = []
    # Find all occurrences of word in subtitle line
    subLine = " "+" ".join(subLine)+" "
    word = " "+word+" "
    # Credit to http://stackoverflow.com/questions/4664850/find-all-occurrences-of-a-substring-in-python
    occurrences = [(m.start(),m.end()) for m in re.finditer(word, subLine)]
    print(occurrences)
    # Take proportional chunk out of timeRange
    lineLength = len(subLine)
    startSeconds = float(timeRange[0][0][3:5])*60 + float(timeRange[0][0][6:8])
    endSeconds = float(timeRange[1][0][3:5])*60 + float(timeRange[1][0][6:8])
    secondsOfRange = endSeconds - startSeconds
    for (startCharIdx,endCharIdx) in occurrences:
        # Assumes HH:MM:SS possibly with decimal places.
        wordStartSeconds = startSeconds+(startCharIdx/lineLength)*secondsOfRange
        wordEndSeconds = endSeconds+(endCharIdx/lineLength)*secondsOfRange



        timeRanges.append((wordStartSeconds,wordEndSeconds))


    return timeRanges

def wordOccurrences(subs, words, singleWords=False, fakeSpeech=False):
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
    print words
    for idx, wordList in enumerate(segmentedWordList):
        for word in words:
            if word.upper() in map(str.upper,wordList):
                if singleWords:  # User chooses to have only one word per clip
                    timeRanges = refineBounds(word, wordList, times[idx])
                else:
                    timeRanges = [times[idx]]
                occurrences += timeRanges
                # You only add whole line once
                if not singleWords:
                    break

    return occurrences


# ---------==== Step 3 ====---------- #

def slice_video(video,timeRanges):
    """
    We use Zulko's excellent moviepy, and a line from
    http://zulko.github.io/blog/2014/06/21/some-more-videogreping-with-python/
    """
    # print timeRanges
    return concatenate([video.subclip(start, end)
                         for (start,end) in timeRanges])

# ---------==== Step 4 ====---------- #

def save_video(fname,video):
    """
    Save the video to "out/"+fname
    """
    video.write_videofile("output/"+fname+"-sliced.mp4", fps=video.fps,
                  codec='libx264', audio_codec='aac',
                  temp_audiofile= 'output/temp-audio.m4a',
                  remove_temp=True, audio_bitrate="1000k", bitrate="4000k")

# ---------===== MAIN ====---------- #

NAME = "1"
WORDS = ["Americans"]
FUNCTION_CHOSEN = 1

# USER OPTIONS
#    1) Entire Subtitle Line                      [done]
#        a) Enhancement: Refine to sentences.     []
#    2) Specific Word(s)                          []
#        a) Enhancement: Refine bounds using
#           sound alignment.                      []
#    3) String of individual words (fake speech)  []

def main():
    # STEP 1: Load files
    video = loadVideo(NAME)
    subs = loadSubs(NAME)
    # STEP 2: Process Subs Into Array
    word_occurrences = wordOccurrences(subs, WORDS)
    # STEP 3: Slice the Video
    video = slice_video(video, word_occurrences)
    # STEP 4: Save the Video that has been cut.
    save_video(NAME,video)


def test():
    subs = loadSubs(NAME)
    timestamps = wordOccurrences(subs, WORDS)
    print subs
    print timestamps

def test2():
    subs = loadSubs('Obama-African-Union')
    timestamps = wordOccurrences(subs, 'Africa')
    print subs
    print timestamps

def test3():
    subLine = "But it is clear that the two of them had gone down the".split(" ")
    timeRange = ["00:00:56,489"],["00:00:59,592"]
    word = "the"
    print refineBounds(word, subLine, timeRange)

if __name__ == '__main__':
    # test()
    # test2()
    test3()
    # main()




