class Ticket:
    def __init__(self,line):
        parts = line.split(':')[1].split('|')
        self.winingNumbers = list(filter(None ,parts[0].split(' ')))
        self.numbers = list(filter(None ,parts[1].split(' ')))
        
        self.score = 0
        self.copies = 1
        self.matchCount = 0

        for n in self.numbers:
            if n in self.winingNumbers:
                self.matchCount += 1
        
        if self.matchCount > 0:
            self.score = pow(2,self.matchCount-1)
    