
from enum import unique
import re
import statistics

def part_one(file):
    image = read_file(file)
    
    image.print()

    image.enhance(2)
    image.print()
    
    print('P1 ' + file + ': ' + str(image.count()))
    
    
def part_two(file):
    image = read_file(file)

    image.enhance(50)
    image.print()
    
    print('P2 ' + file + ': ' + str(image.count()))
    

def read_file(file):
    file_contents = open("./input/" + file, "r").read().splitlines()
    
    image = Image(file_contents[0])
    for line in file_contents[2:]:
        image.addLine(line)

    return image



class Image:
    def __init__(self, algo):
        self.lines = []
        self.algo = algo
        self.outOfBoundChar = '.'

    def addLine(self,line):
        self.lines.append(line)
    
    def print(self):
        print()
        for line in self.lines:
            print(line)
        print()

    def addPadding(self,count):
        for i in range(0,count):
            w = len(self.lines[0])+2
            
            lines = ['.'*w]
            for line in self.lines:
                lines.append('.'+line+'.')
            lines.append('.'*w)

            self.lines = lines
    
    def getPixel(self,x,y):
        if x < 0 or y < 0 or y > len(self.lines) - 1 or x > len(self.lines[y]) - 1:
            return self.outOfBoundChar
        return self.lines[y][x]

    def getEnhancedPixel(self,x,y):

        total = self.getPixel(x-1,y-1) + self.getPixel(x,y-1) + self.getPixel(x+1,y-1) 
        total += self.getPixel(x-1,y) + self.getPixel(x,y) + self.getPixel(x+1,y) 
        total += self.getPixel(x-1,y+1) + self.getPixel(x,y+1) + self.getPixel(x+1,y+1) 

        return self.lookupPixelString(total)  
        
    def lookupPixelString(self,pixelString):        
        byte = pixelString.replace('#','1').replace('.','0')
        return self.algo[int(byte,2)]

    def createSpace(self,minSpace):
        top = 0
        bottom = 0
        left = -1
        right = -1

        fillChar = '#'
        if self.outOfBoundChar == '#':
            fillChar = '.'

        # Set top
        for line in self.lines:           
            if line.count(fillChar) > 0:
                break
            top += 1
        
        j = len(self.lines) - 1
        while j > 0:
            if self.lines[j].count(fillChar) > 0:
                break
            bottom += 1
            j -= 1
        
        for i in range(top,len(self.lines)-bottom):
            lineLeft = 0
            lineRight = 0
            line = self.lines[i]
            for char in line:
                if char == fillChar:
                    break
                lineLeft += 1
            
            j = len(line) - 1
            while j > 0:
                if line[j] == fillChar:
                    break
                lineRight += 1
                j -= 1
            
            if left < 0:
                left = lineLeft
            else:
                left = min(lineLeft,left)
            
            if right < 0:
                right = lineRight
            else:
                right = min(lineRight,right)

        lines = []
        
        for line in self.lines:
            if left < minSpace:
                line = self.outOfBoundChar*(minSpace-left) + line
            if right < minSpace:
                line += self.outOfBoundChar*(minSpace-right)
            lines.append(line)

        emptyLine = self.outOfBoundChar * len(lines[0])
        if bottom < minSpace:
            moreLines = [emptyLine]*(minSpace-bottom)
            lines += moreLines
            
        if top < minSpace:
            moreLines = [emptyLine]*(minSpace-top)
            lines = moreLines + lines
            
        self.lines = lines

    def enhance(self,count):
        for i in range(0,count):
            self.createSpace(4)
            lines = []
            for y in range(0,len(self.lines)):
                line = ''
                for x in range(0,len(self.lines)):
                    line += self.getEnhancedPixel(x,y)
                # line += '.'
                lines.append(line)

            self.lines = lines

            #Set out of bounds char:
            outByte = 9*self.outOfBoundChar
            self.outOfBoundChar = self.lookupPixelString(outByte)
        
    def count(self):
        count = 0
        for line in self.lines:
            count += line.count('#')
        return count

part_one('test.txt')
part_one('real.txt')
part_two('test.txt')
part_two('real.txt')
