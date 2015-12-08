from utils import parseSRT

# ---------==== Step 1 ====---------- #

def loadVideo(fname):
    """
    Probably an array of images + audio, right?
    We'll have to investigate.
    """
    return 0

def loadSubs(fname):
    """
    Returns an instance of the Subtitle Class
    """
    return parseSRT(fname)

# ---------==== Step 2 ====---------- #

def wordOccurrences(subs, word):
    """
    subs is a dictionary with keys of integers (0, N)
    subs.data[0] --> {"timestamp": timestamp, "text": text}
    subs.words[0] --> ['word1', 'word2']
    subs.times[0] --> ['00:00:00 --> 00:00:04']

    Returns an array of tuples denoting
    the time-ranges when WORD occurs.

    We search for WORD:
    - Not Case-Sensitive.
    - Only exact matches of the word
      - (i.e. "african" should not be found for the word "africa").

    For example:
        [("00:01:05","00:01:11"),("00:01:28","00:01:37")]
    """
    # occurrences_list = [("00:01:05","00:01:11"),("00:01:28","00:01:37")]
    segmentedWordList = subs.words
    times = subs.times
    occurrences = []
    for idx, wordList in enumerate(segmentedWordList):
        # idx is index
        if word in wordList:
            # Refine bounds for TIMES
            occurrences.append(times[idx])

    return occurrences

def sections_to_remove(word_occurrences):
    """
    WORD_OCCURRENCES is a time-ordered array
    of tuples.
        [("00:01:05","00:01:11"), ...]

    Return SECTIONS_TO_REMOVE. Every time-range
    between the time-ranges in WORD_OCCURRENCES.

    e.g. [("00:00:00","00:01:05"),("00:01:11",...), ...]
    """
    sections_to_remove = [("00:00:00","00:01:05")]
    return sections_to_remove

# ---------==== Step 3 ====---------- #

def slice_video(video,sections_to_remove):
    """
    VIDEO is structured as a... 3d array?

    SECTIONS_TO_REMOVE is all time-ranges that
    we are not keeping and should therefore delete.

    Since VIDEO is large, we delete irrelevant
    sections of VIDEO, rather than making a copy.
    """
    for section in sections_to_remove:
        # delete that particular time-range
        pass

# ---------==== Step 4 ====---------- #

def save_video(fname):
    """
    Save the video to "out/"+fname
    """
    pass

# ---------===== MAIN ====---------- #

NAME = "Intro"
WORD = "say"

def main():
    # STEP 1: Load files
    video = loadVideo(NAME + '.mp4')
    subs = loadSubs(NAME)

    # STEP 2: Process Subs Into Array
    word_occurrences = wordOccurrences(subs, WORD)
    sections_to_remove = sections_to_remove(word_occurrences)

    # STEP 3: Slice the Video
    slice_video(video,sections_to_remove)

    # STEP 4: Save the Video that has been cut.
    save_video = save_video(video_name+"-cut.jpg")

def test():
    subs = loadSubs(NAME)
    timestamps = wordOccurrences(subs, WORD)
    print subs
    print timestamps

def test2():
    subs = loadSubs('Obama-African-Union')
    timestamps = wordOccurrences(subs, 'Africa')
    print subs
    print timestamps

if __name__ == '__main__':
    # test()
    test2()