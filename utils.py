# internals
from classes import SubtitleClass
from classes import WordTokenizer as wdtk

INPUT_FOLDER = 'data/'
OUTPUT_FOLDER = 'output/'

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
    parsed = [ lines[i:i+2] for i in range(1, len(lines), 4) ]
    dataDict = {}
    with open(OUTPUT_FOLDER + fname + '.txt', 'w') as outfile:
        for idx, line in enumerate(parsed):
            timestamp, text = line
            translations = [ ['&#39;', "'"], # apostrophe
                             ['&gt;', ">"], # greater than sign
                            ]
            for orginal, translated in translations:
                text = text.replace(orginal, translated)  # translate junk
            dataDict[idx] = {"timestamp": timestamp, "text": text}
            outfile.writelines(timestamp+text)
    Subtitles = SubtitleClass(fname, dataDict)
    print(Subtitles)
    print 'Total Number of words: %d | Uniques: %d' % (Subtitles.wordCount, Subtitles.uniqueWordCount() )

if __name__ == '__main__':
    parseSRT('Intro')