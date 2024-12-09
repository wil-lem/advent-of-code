import re
from readFile import ReadFile

class Equation:
    def __init__(self,parts):
        self.total = int(parts.pop(0))
        self.parts = parts
        self.operators = ['+','*']
        self.allowConcetenation = False
        
    def setAllowConcetenation(self):
        self.allowConcetenation = True
        self.operators.append('|')

    def getValidCount(self):
        total = int(self.parts[0])
        return self.getValidTotalsCount(total,1)

    def getValidTotalsCount(self,currentTotal,index):
        count = 0
        if currentTotal > self.total:
            return 0
        nextValue = int(self.parts[index])
        for op in self.operators:
            if op == '+':
                total = currentTotal + nextValue
                if index+1 < len(self.parts):
                    count += self.getValidTotalsCount(total,index+1)
                else:
                    if total == self.total:
                        count += 1
            elif op == '*':
                total = currentTotal * nextValue
                if index+1 < len(self.parts):
                    count += self.getValidTotalsCount(total,index+1)
                else:
                    if total == self.total:
                        count += 1
            elif op == '|':
                total = int(str(currentTotal) + str(nextValue))
                if index+1 < len(self.parts):
                    count += self.getValidTotalsCount(total,index+1)
                else:
                    if total == self.total:
                        count += 1
        return count
    
def parseFile(filename):
    rf = ReadFile(filename)
    lines = rf.getLines()
    
    equations = []
    for line in lines:
        digits = re.findall(r'(\d+)',line)
        equations.append(Equation(digits))
    return equations


def one(filename):
    equations = parseFile(filename)
    total = 0
    for eq in equations:
        if eq.getValidCount() > 0:
            total += eq.total
       
        
    print('Total:', total)
        
def two(filename):
    equations = parseFile(filename)
    total = 0
    for eq in equations:
        eq.setAllowConcetenation()
        if eq.getValidCount() > 0:
            total += eq.total
       
        
    print('Total:', total)
    
    
one(ReadFile.testFile())
one(ReadFile.realFile())
two(ReadFile.testFile())
two(ReadFile.realFile())