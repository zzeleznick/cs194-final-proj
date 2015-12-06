# ---------==== Step 1 ====----------

def load_video(fname):
    """
    Probably an array of images + audio, right?
    We'll have to investigate.
    """
    return 0

def load_subs(fname):
    """
    Returns a long string, I'm thinking.
    (maybe a buffer?)
    """
    return 0

# ---------==== Step 2 ====----------

def word_occurrences(subs,word):
    """
    SUBS is a string.

    Returns an array of tuples denoting
    the time-ranges when WORD occurs.

    We search for WORD:
    - Not case-sensitive.
    - Only the word (i.e. "african" should
      not be found for the word "africa").

    For example:
        [("00:01:05","00:01:11"),("00:01:28","00:01:37")]
    """
    occurrences_list = [("00:01:05","00:01:11"),("00:01:28","00:01:37")]
    return occurrences_list

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

# ---------==== Step 3 ====----------

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

# ---------==== Step 4 ====----------

def save_video(fname):
    """
    Save the video to "out/"+fname
    """
    pass

# ---------=========----------

video_name = "1"
word = "africa"

def main():
    # STEP 1: Load files
    video = loadVideo(video_name+".jpg")
    subs = load_subs(video_name+".srt")
    # STEP 2: Process Subs Into Array
    word_occurrences = word_occurrences(subs,word)
    sections_to_remove = sections_to_remove(word_occurrences)
    # STEP 3: Slice the Video
    slice_video(video,sections_to_remove)
    # STEP 4: Save the Video that has been cut.
    save_video = save_video(video_name+"-cut.jpg")

if __name__ == '__main__':
    main()