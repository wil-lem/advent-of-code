class ConversionMap:
    def __init__(self,lines):
        title = lines[0].split(' ')[0].split('-to-')
        self.sourceName  = title[0]
        self.targetName = title[1]
        self.ranges = []

        for line in lines[1:]:
            self.ranges.append(ConversionRange(line))
        self.ranges.sort(key=lambda r: r.getSourceStart())

    def __str__(self) -> str:
        strRanges = map(str,self.ranges)
        return self.sourceName + '->'  + self.targetName + ': \n  ' + '\n  '.join(strRanges)    
    
    def convert(self,n):
        for r in self.ranges:
            if r.inRange(n):
                return r.convert(n)
        return n

    def convertRanges(self,ranges):
        # We want to go through al ranges and convert the ranges
        # sending on range, might chop up a range and return more ranges
        newRanges = []

        for cr in self.ranges:
            remainders = []
            for r in ranges:
                data = cr.convertRange(r)
                converted = data[0]
                if data[0]:
                    newRanges.append(converted)
                remainders += data[1][:]
            ranges = remainders

        newRanges += ranges
        
        return newRanges
    
class ConversionRange:
    def __init__(self, line):
        parts = line.split(' ')
        self.sourceRange = NumberRange(int(parts[1]), int(parts[2])-1)
        self.targetRange = NumberRange(int(parts[0]), int(parts[2])-1)
        
    def __str__(self) -> str:
        return str(self.sourceRange) + ' -> ' + str(self.targetRange)

    def inRange(self,n):
        return self.sourceRange.contains(n)
    
    def convert(self,n):
        pos = self.sourceRange.getPos(n)
        return self.targetRange.getValue(pos)
    
    def getSourceStart(self):
        return self.sourceRange.start

    def convertRange(self, r):
        # We want to return to list
        # - Converted [ranges]
        # - Remainder [ranges]
        
        overlap = self.sourceRange.getOverlap(r)
        if overlap == False:
            remaining = [r.clone()]
            converted = []
        else:
            converted = NumberRange(self.convert(overlap.start),overlap.length)
            remaining = r.substract(overlap)

        
        return [converted,remaining]
    

class NumberRange:
    def __init__(self,s,l) -> None:
        self.start = s
        self.length = l
        self.end = s + l
    
    def __str__(self) -> str:
        return str(self.start) + '-' + str(self.end) + ' (l: ' + str(self.length) + ')'
    
    def contains(self,n):
        return (self.start <= n and self.end >= n)

    def getPos(self,n):
        return n - self.start
    
    def getValue(self,pos):
        return self.start + pos
    
    def getOverlap(self,otherRange):
        if self.contains(otherRange.start):
            if(self.contains(otherRange.end)):
                return otherRange.clone()
            else:
                return NumberRange.fromStartEnd(otherRange.start,self.end)
        else:
            if(self.contains(otherRange.end)):
                return NumberRange.fromStartEnd(self.start,otherRange.end)
        
        if otherRange.contains(self.start) and otherRange.contains(self.end):
            return self.clone()

        return False
                
    def fromStartEnd(s,e):
        return NumberRange(s,e-s)

    def clone(self):
        return NumberRange(self.start,self.length)
    
    def substract(self,otherRange):
        parts = []

        if self.contains(otherRange.start):
            parts.append(NumberRange.fromStartEnd(self.start,otherRange.start-1))
            if(self.contains(otherRange.end)):
                parts.append(NumberRange.fromStartEnd(otherRange.end+1,self.end))
        else:
            if(self.contains(otherRange.end)):
                parts.append(NumberRange.fromStartEnd(self.otherRange.end+1,self.end))
        
        return list(filter(lambda r: r.length > 0,parts))