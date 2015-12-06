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
        def buildFreqDist(dataDict):
            fullText = ''.join([entry['text'] for entry in dataDict.values()])
            fullText = fullText.replace('\n', ' ')
            words = WordTokenizer(fullText).tokenize()
            freqDist = {}
            totalWords = 0
            for word in words:
                totalWords += 1
                if word not in freqDist:
                    freqDist[word] = 1
                else:
                    freqDist[word] += 1
            return freqDist, totalWords

        self.name = name
        self.data = dataDictionary
        self.freqDist, self.wordCount = buildFreqDist(dataDictionary)
        self.lineCount = len(self.data.keys())

    def uniqueWordCount(self):
        return len(self.freqDist.keys())

    def __repr__(self):
        return '<SubtitleObj: %s | lines: %d | words: %d>' %  (self.name, self.lineCount, self.wordCount)

    def __str__(self):
        return repr(self)
