from utils import parseSRT
from moviepy.editor import VideoFileClip, concatenate

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

# ---------==== Step 3 ====---------- #

def slice_video(video,timeRanges):
    """
    We use Zulko's excellent moviepy, and a line from
    http://zulko.github.io/blog/2014/06/21/some-more-videogreping-with-python/
    """
    print timeRanges
    return concatenate([video.subclip(start, end)
                         for (start,end) in timeRanges])

# ---------==== Step 4 ====---------- #

def save_video(fname,video):
    """
    Save the video to "out/"+fname
    """
    video.write_videofile("output/"+fname+'.mp4', fps=video.fps,
                  codec='libx264', audio_codec='aac',
                  temp_audiofile= 'output/temp-audio.m4a',
                  remove_temp=True, audio_bitrate="1000k", bitrate="4000k")

# ---------===== MAIN ====---------- #

NAME = "1"
WORD = "Africa"

def main():
    # STEP 1: Load files
    video = loadVideo(NAME)
    subs = loadSubs(NAME)
    # STEP 2: Process Subs Into Array
    word_occurrences = wordOccurrences(subs, WORD)
    # STEP 3: Slice the Video
    video = slice_video(video, word_occurrences)
    # STEP 4: Save the Video that has been cut.
    save_video(NAME,video)


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
    # test2()
    main()




