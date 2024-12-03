
class Node():
    def __init__(self,v):
        self.v = v
        self.char = False
        self.connections = []
        self.distance = 0

    def __str__(self) -> str:
        return self.char + ' - ' + str(self.v) + ' (d:' + str(self.distance) + ')'
     
    def setChar(self,c):
        self.char = c

    def connectNode(self,other):
        if other not in self.connections:
            self.connections.append(other)
        if self not in other.connections:
            other.connections.append(self)

    def scanAround(self,points):
        possiblePoints = self.getSurroundingVectors(Vector(len(points[0])-1,len(points)-1))
        
        found = []
        for v in possiblePoints:
            connected = v.getConnecting(points[v.y][v.x])
            
            if connected and (connected[0] == self.v or connected[1] == self.v):
                found.append(v)
        return found
    
    def getSurroundingVectors(self,maxV):
        return self.v.getSurroundingVectors(maxV)
        
    def next(self):
        if len(self.connections) != 1:
            return False

        connecting = self.v.getConnecting(self.char)
        for v in connecting:
            if v != self.connections[0].v:
                n = Node(v)
                n.distance = self.distance + 1
                return n        
        return False
    
    def isCorner(self):
        return self.char not in ['-','|']
    
class Vector:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def __eq__(self, other: object) -> bool:
        return self.x == other.x and self.y == other.y
    
    def __str__(self) -> str:
        return '[' + str(self.x) + ', ' + str(self.y) + ']'
    
    def getSurroundingVectors(self,maxV):
        surrounding = []
        if self.y > 0:
            surrounding.append(Vector(self.x,self.y-1))
        if self.y < maxV.y:
            surrounding.append(Vector(self.x,self.y+1))
        if self.x > 0:
            surrounding.append(Vector(self.x-1,self.y))
        if self.x < maxV.x:
            surrounding.append(Vector(self.x+1,self.y))
        return surrounding

    def getConnecting(self,c):
        a = Vector(self.x,self.y)
        b = Vector(self.x,self.y)

        if c == '|':
            a.y -= 1
            b.y += 1
        if c == '-':
            a.x -= 1
            b.x += 1
        if c == 'L':
            a.y -= 1
            b.x += 1
        if c == 'J':
            a.y -= 1
            b.x -= 1
        if c == 'F':
            a.y += 1
            b.x += 1
        if c == '7':
            a.y += 1
            b.x -= 1
        if a == self and b == self:
            return False

        return [a,b]

class Polygon:
    def __init__(self) -> None:
        self.points = []

    def add(self,v):
        self.points.append(v)

    
    def __str__(self) -> str:
        return ' '.join(list(map(str,self.points)))
        
    def getArea(self):
        print(self)
        # Say we have a simple square:
        # 0,0 2,0 2,2 0,2 - This would have 1 dot but if we would calculate the area it would be 4 (2x2)
        # 0,0 4,0 4,3 0,3 - 6 dots (3x2) instead of 4x3.
        # So we have to do something with the offset of 1
        # What if there's a corner missing
        # 0,0 4,0 4,2 3,2 3,3 0,3 = 5 dots (3x2 - 1x1) instead of 11

        # It has to do with constantly forming potential squares. Taking above example:
        # [0,0] = no potential
        # [4,0] = 1 line [0,0]-[4-0]
        # [4,2] = potential square [0,0]x[3,1]
        # [3,2] = potential square [0,0]x[3,1]
        # [3,3] = potential square [0,0]x[3,1] + [2,1]


        return 1