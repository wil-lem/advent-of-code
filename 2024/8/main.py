import re
from readFile import ReadFile
    

class Vector:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        pass
    
    def diff(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def distance(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

    def multiply(self, value):
        return Vector(self.x * value, self.y * value)

    def add(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    
    def inGrid(self, w, h):
        return self.x >= 0 and self.x < w and self.y >= 0 and self.y < h

    def clone(self):
        return Vector(self.x, self.y)

    def __eq__(self, value):
        return self.x == value.x and self.y == value.y
    
    def __str__(self):
        return f'({self.x},{self.y})'

class Line:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        pass
    
    
class Antenna:
    def __init__(self, freq,x,y):
        self.freq = freq
        self.pos = Vector(x,y)
        self.parents = []
        self.children = []
        self.antinodes = []
        pass
    
    def addChild(self, antenna):
        self.children.append(antenna)

    def generateAntinodes(self):
        for child in self.children:
            diff = self.pos.diff(child.pos)
            antinode = self.pos.add(diff)
            diff = diff.multiply(-1)
            antinode2 = child.pos.add(diff)
            self.antinodes.append(antinode)
            child.antinodes.append(antinode2)
    
    def generateAllAntinodes(self,w,h):
        for child in self.children:
            startPos = self.pos.clone()
            diff = self.pos.diff(child.pos)
            while(startPos.inGrid(w,h)):
                self.antinodes.append(startPos.clone())
                startPos = startPos.add(diff)

            startPos = child.pos.clone()
            diff = diff.multiply(-1)
            while(startPos.inGrid(w,h)):
                child.antinodes.append(startPos.clone())
                startPos = startPos.add(diff)
         
    def __str__(self):
        return f'{self.freq} at {self.pos.x},{self.pos.y} with {len(self.children)} children and {len(self.parents)} parents'
    
def parseFile(filename):

    rf = ReadFile(filename)
    lines = rf.getLines()
    w = 0
    h = len(lines)
    antennas = []

    for y in range(len(lines)):
        w = len(lines[y].strip())
        for x in range(len(lines[y])):
            char = lines[y][x]
            if re.match(r'[a-zA-Z0-9]', char):
                antenna = Antenna(char, x, y)
                sameFrequency = [a for a in antennas if a.freq == antenna.freq]
                for a in sameFrequency:
                    a.addChild(antenna)               
                antennas.append(antenna)
    return antennas,w,h

def one(filename):
    antennas,w,h = parseFile(filename)

    uniqueAntinodes = []
    for ant in antennas:
        ant.generateAntinodes()
        for antinode in ant.antinodes:
            if antinode not in uniqueAntinodes:
                uniqueAntinodes.append(antinode)

    uniqueAntinodes = [ant for ant in uniqueAntinodes if ant.inGrid(w,h)]
    print('Total:', len(uniqueAntinodes))

        
def two(filename):
    antennas,w,h = parseFile(filename)

    uniqueAntinodes = []
    for ant in antennas:
        ant.generateAllAntinodes(w,h)
        for antinode in ant.antinodes:
            if antinode not in uniqueAntinodes:
                uniqueAntinodes.append(antinode)

    uniqueAntinodes = [ant for ant in uniqueAntinodes if ant.inGrid(w,h)]
    print('Total:', len(uniqueAntinodes))
    
    
one(ReadFile.testFile())
one(ReadFile.realFile())
two(ReadFile.testFile())
two(ReadFile.realFile())