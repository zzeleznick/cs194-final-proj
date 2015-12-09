import time
import datetime
import re

class SampleData:
    """Class for testing refineBounds"""
    def __init__(self, word, lines, timeRanges):
        self.times = timeRanges # [ ("00:00:56,489","00:00:59,592"), ... ]
        self.lines = lines # [ ['But', 'it', 'is', 'clear', 'that', 'the', 'two', 'of', 'them', 'had', 'gone', 'down', 'the'], ...]
        self.word = word
        assert len(self.lines) == len(self.times), 'mismatch lengths for lines: %d and times: %d' % (len(self.lines), len(self.times))

    def refineBoundsAllLines(self):
        out = {}
        out2 = {}
        for i in range(len(self.lines)):
            line, timeRange = self.lines[i], self.times[i]
            print 'Iteration: %d\nline: %s\ntimeRange: %s' % (i, line, timeRange)
            out.update({i: refineBoundsSingleLine(self.word, line = line, timeTuple = timeRange) })
            # out2.update({i: refineBounds(self.word, line, timeRange) })
        return out #, out2


def refineBoundsSingleLine(word, line, timeTuple, padding = .10):
    # timeTuple = ("00:00:56,489", "00:00:59,592")
    timeRanges = []
    # Find all occurrences of word in subtitle line
    subLine = " " + " ".join(line) + " "  # no fuzzy matches by adding spaces
    word = " " + str(word) + " "
    # Credit to http://stackoverflow.com/questions/4664850/find-all-occurrences-of-a-substring-in-python
    occurrences = [(m.start(),m.end()) for m in re.finditer(word, subLine)]
    start, end = timeTuple
    # print 'start: %s, end: %s' % (start, end)
    base = datetime.datetime.strptime('00:00:00,000', "%H:%M:%S,%f")
    epoch = datetime.datetime.fromtimestamp(0)
    timeadjust = (epoch - base).total_seconds()
    st, ed = [ datetime.datetime.strptime(var, "%H:%M:%S,%f") for var in [start, end] ]
    st, ed = [(dt - base).total_seconds() for dt in [st, ed]]
    duration = ed - st
    print line
    print timeTuple
    for m_start, m_end in occurrences:
        print "Character group: %s-%s, start: %0.2f, end: %0.2f " % (m_start, m_end, st, ed)
        offset =  float(m_start)/len(subLine)
        padding *= (1 + 4.0 / duration**2)
        if offset < .5:
            true_start = st + offset * duration  - padding * 2 * ( .5 + offset)
            true_end = st + float(m_end)/len(subLine) * duration + padding
        else:
            true_start = ed - (1 - offset) * duration  - padding * 4 * ( .5 + offset )
            true_end = ed - (1 - (float(m_end)/len(subLine)) ) * duration + padding

        ts, te = [ datetime.datetime.fromtimestamp(val - timeadjust) for val in [true_start, true_end] ]
        # ts, te = [ str(dt).split()[1][:-3].replace('.', ',') for dt in [ts, te]]
        ts, te = [ str(dt).split()[1][:-3] for dt in [ts, te]]
        print ts, te
        timeRanges.append([ts, te])

    return timeRanges

def refineBounds(word, subLine, timeRange, padding=0.1):
    """
    subLine = "But it is clear that the two of them had gone down the"
    timeRange = ["00:00:56,489","00:00:59,592"]
    word = "the"
    """
    timeRanges = []
    # Find all occurrences of word in subtitle line. Add spaces to find exact words.
    subLine = " "+" ".join(subLine)+" "
    word = " "+word+" "
    # Credit to http://stackoverflow.com/questions/4664850/find-all-occurrences-of-a-substring-in-python
    occurrences = [(m.start(),m.end()) for m in re.finditer(word, subLine)]
    print(occurrences)
    # Take the lenth of the string.
    lineLength = float(len(subLine))
    # Convert start and end time of subLine to floats of seconds
    startRange = datetime.datetime.strptime(timeRange[0], "%H:%M:%S,%f")
    endRange = datetime.datetime.strptime(timeRange[1], "%H:%M:%S,%f")
    # Convert to timeDelta
    # startRange = float(startRange.second) + float(startRange.microsecond/1000)
    # endRange = float(startRange.second) + float(startRange.microsecond/1000)
    secondsOfRange = (endRange-startRange).total_seconds()
    start = (startRange - datetime.datetime.fromtimestamp(0)).total_seconds()
    for (startCharIdx,endCharIdx) in occurrences:
        wordStartSecs = (float(startCharIdx)/lineLength)*secondsOfRange
        wordEndSecs = (float(endCharIdx)/lineLength)*secondsOfRange
        # Convert each to dateTime object and add the start time
        wordStartSecs = start + datetime.datetime.strptime(str(wordStartSecs), "%S.%f")
        wordEndSecs = start + datetime.datetime.strptime(str(wordEndSecs), "%S.%f")
        # Finally add to timeRanges
        timeRanges.append((wordStartSecs.toString("HH:mm:ss"),wordEndSecs.toString("HH:mm:ss")))
    return timeRanges

def test():
    timeRanges = [ ("00:00:56,489", "00:00:59,592"),
                    ("00:01:06,489", "00:01:19,091"),
                    ("00:03:30,500", "00:03:40,500"),
                     ("00:32:46,489","00:32:59,091"),
                    ]
    lines = [ ['But', 'it', 'is', 'clear', 'that', 'the', 'two', 'of', 'them', 'had', 'gone', 'down', 'the'],
                ['somedays', 'I', 'really', 'hate', 'the', 'code', 'for', 'these', 'projects', 'and', 'the', 'like'],
                ['though', 'I', 'cannot', 'say', 'that', 'we', 'are', 'doomed', 'to', 'fail'],
                ['since', 'we', 'are', 'all', 'special', 'as', 'the', 'snowflakes', 'in', 'the', 'sky', 'and', 'the', 'water'],
            ]
    word = 'the'
    print "Testing word grep on '%s' for %d lines" % (word, len(lines))
    sample = SampleData(word, lines, timeRanges)
    print sample.refineBoundsAllLines()

if __name__ == '__main__':
    test()