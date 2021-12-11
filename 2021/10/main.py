from enum import unique
import re
import statistics

def part_one(file):
    lines = read_file(file)
    
    count = 0
    for line in lines:
        for chunk in line.chunks:
            count += chunk.getSyntaxErrorScore()


    print('P1 ' + file + ': ' + str(count))
    
    
def part_two(file):
    lines = read_file(file)
    
    scores = []
    for line in lines:
        
        if line.hasSyntaxErrors():
            continue

        for chunk in line.chunks:
            score = chunk.getCompletionScore()
            if score > 0:
                scores.append( score )   
    
    
    print('P2 ' + file + ': ' + str(statistics.median(scores)))


def read_file(file):
    file_contents = open("./input/" + file, "r").read().splitlines()
    
    lines = []
    for num,line in enumerate(file_contents):
        line = Line(num,line)
        lines.append(line)
    return lines

    
class Line:
    def __init__(self,num,text) -> None:
        self.text = text
        self.num = num
        self.chunks = []
        self.addChunks()

    def addChunks(self):
        text = self.text
        while text != '':
            chunk = Chunk(text)
            self.chunks.append(chunk)
            if chunk.parse() == False:
                break

            text = chunk.getRemainder()
            if(text != ''):
                text = text[1:]
    def hasSyntaxErrors(self):
        score = 0
        for chunk in self.chunks:
            score += chunk.getSyntaxErrorScore()
        return score > 0

class Chunk:
    def __init__(self,text):
        self.closedIndex = 0
        self.children = []

        self.text = text
        self.openChar = text[0:1]
        self.innerText = False
        self.closeChar = False
        
        self.syntaxError = False
        self.remainder = False

    def isEmpty(self):
        return self.text == ""

    def isClosed(self):
        return self.closedIndex > 0

    def getOpenChar(self):
        if self.openChar in ['[','{','(','<']:
            return self.openChar
        return False
    
    def getDefaultCloseChar(self):
        start = self.getOpenChar()
        if start == '[':
            return ']'
        if start == '{':
            return '}'
        if start == '(':
            return ')'
        if start == '<':
            return '>'
        return False
    
    def getOuterText(self):
        return self.openChar + self.innerText + self.closeChar
    
    def getLength(self):
        return len(self.innerText) + 2

    def getRemainder(self):
        return self.text[self.getChildrenLength() + 1:]

    def getChildrenLength(self):
        total = 0
        for child in self.children:
            total += child.getLength()
        return total

    def closeIt(self):
        self.innerText = ''
        childLength = self.getChildrenLength()
        if childLength > 0:
            self.innerText = self.text[1:childLength+1]

        self.closeChar = self.getRemainder()[0:1]

    def parse(self):
        
        if self.isEmpty():
            #Nothing to do here
            return False

        if self.getOpenChar() == False:
            self.syntaxError = True
            # Syntax error
            return False


        remainder = self.getRemainder()
        while len(remainder) > 0:
            if remainder[0:1] == self.getDefaultCloseChar():
                self.closeIt()
                return True

            chunk = Chunk(remainder)
            self.children.append(chunk)
            
            if chunk.parse() == False:
                return False
            
            remainder = self.getRemainder()
        
        return False

    def debug(self,prefix):
        print(prefix,self.openChar,'--',self.innerText,'--')

        for chunk in self.children:
            if chunk.syntaxError:
                print('Syntax error, expecting',self.getDefaultCloseChar(),',got',chunk.text[0:1])
                break
            chunk.debug(prefix+'.')
        print(prefix,self.closeChar)
    def getSyntaxError(self):
        if self.syntaxError:
            print('Found syntax error',self.text[0:1])
            return True
        for chunk in self.children:
            if chunk.getSyntaxError():
                return True
        return False
    def getSyntaxErrorScore(self):
        if self.syntaxError:
            char = self.text[0:1]
            if char == ')':
                return 3
            if char == ']':
                return 57
            if char == '}':
                return 1197
            if char == '>':
                return 25137
            print('False syntax error')
        for chunk in self.children:
            score = chunk.getSyntaxErrorScore()
            if score > 0:
                return score
        return 0
    def getCompletionScore(self):
        score = 0
        for chunk in self.children:
            score += chunk.getCompletionScore() * 5


        if self.closeChar == False:
            if self.getDefaultCloseChar() == ')':
                score += 1
            if self.getDefaultCloseChar() == ']':
                score += 2
            if self.getDefaultCloseChar() == '}':
                score += 3
            if self.getDefaultCloseChar() == '>':
                score += 4
        
        return score
            

    

            
    
part_one('test.txt')
part_one('real.txt')
part_two('test.txt')
part_two('real.txt')
