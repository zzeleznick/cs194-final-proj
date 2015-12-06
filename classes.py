class SubtitleClass:
    """Class for handling srt files and returning a dictionary like object"""
    def __init__(self, name, dataDictionary):
        def getLineCount(dataDict):
            return len(dataDict.keys())

        def getWordCount(dataDict):
            lines = [entry['text'] for entry in dataDict.values()]
            return sum([len(line.strip().split()) for line in lines])

        self.name = name
        self.data = dataDictionary
        self.lineCount = getLineCount(dataDictionary)
        self.wordCount = getWordCount(dataDictionary)

    def __repr__(self):
        return '<SubtitleObj: %s | lines: %d | words: %d>' %  (self.name, self.lineCount, self.wordCount)

    def __str__(self):
        return repr(self)