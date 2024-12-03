class ReadFile:
    def __init__(self, filename):
        self.filename = filename
        self.file = open(filename, 'r')
        self.lines = self.file.readlines()
        self.file.close()

    def getLines(self):
        return self.lines

    # Static method to get test filename
    @staticmethod
    def testFile():
        return 'input/test.txt'
    
    # Static method to get real filename
    @staticmethod
    def realFile():
        return 'input/real.txt'