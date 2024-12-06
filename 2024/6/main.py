import re
from readFile import ReadFile

def parseFile(filename):
    rf = ReadFile(filename)
    lines = rf.getLines()
    

class Vector:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    
    def set(self,x,y):
        self.x = x
        self.y = y

    def clone(self):
        return Vector(self.x, self.y)

    def move(self,axis,mod):
        if axis == 'x':
            self.x += mod
        else:
            self.y += mod
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return '(' + str(self.x) + ', '+ str(self.y) + ')'
        pass

class Line:
    def __init__(self,x,y):
        self.start = Vector(x,y)
        pass

class Position:
    def __init__(self,x,y,char):
        self.v = Vector(x,y)
        self.char = char
        self.visited = False

    def setVisited(self):
        self.visited = True

    def isOpen(self):
        return self.char != '#'



    def __str__(self):
        return 'Position: ' + str(self.v) + ' C:' + self.char
        pass

class Guard:
    def __init__(self,x,y):
        self.position = Vector(x,y)
        self.axis = 'y'
        self.direction = -1
        self.map = []
        pass

    def nextPosition(self):
        nextPosition = self.position.clone()
        nextPosition.move(self.axis,self.direction)

        matches = [ pos for pos in self.map if pos.v == nextPosition]
        
        if len(matches) == 0:
            return False
        
        return matches[0]

    def turn(self):
        if self.axis == 'y': 
            self.direction *= -1
            self.axis = 'x'
        else:
            self.axis = 'y'
        
        
    def move(self):
        next = self.nextPosition()

        if next == False:
            return False
        if not next.isOpen():
            self.turn()
            # Assume we'll always end up exiting the screen.
            return True
        self.position = next.v.clone()
        next.setVisited()
        return True
    
def one(fileName):
    rf = ReadFile('input/' + fileName + '.txt')
    lines = rf.getLines()
    grid = []
    guard = Guard(0,0)
    for y in range(len(lines)):
        line = lines[y]
        for x in range(len(line) - 1):
            pos= Position(x,y,line[x])
            if pos.char == '^':
                pos.char = '.'
                pos.setVisited()
                guard.position = pos.v.clone()
            guard.map.append(pos)

    move = 0
    while guard.move():
        move += 1

    print('Total:', len([pos for pos in guard.map if pos.visited]))
    
one('test')
one('real')
