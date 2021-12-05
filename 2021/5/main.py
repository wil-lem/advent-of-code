import re

def part_one(file):
    lines = read_file(file)
    map = Map()
    for line in lines:
        if line.isStraight():
            map.addPoints(line.getStraightPoints())
        
    map.doublePointCount()
    
            
def part_two(file):
    lines = read_file(file)
    map = Map()
    for line in lines:
        if line.isStraight():
            map.addPoints(line.getStraightPoints())
        else:
            map.addPoints(line.getDiagonalPoints())

    map.doublePointCount()
    
    
def read_file(file):
    text_file = open("./input/" + file, "r")
    file_contents = text_file.read()
    lines = file_contents.splitlines()

    lines = list(map(parseCoords,lines))

    return lines

def parseCoords(line):
    l = Line(line)
    return l


class Vector:
    def __init__(self,x,y):
        self.x = int(x)
        self.y = int(y)
        self.lineCount = 1
    def print(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ')'

    def equals(self, point):
        return self.x == point.x and self.y == point.y
        

class Line:
    def __init__(self,line):
        matches = re.findall('(\d+)', line)
        
        if(matches):
            self.start = Vector(matches[0],matches[1])
            self.end = Vector(matches[2],matches[3])
    def isStraight(self):
        return self.isHorizontal() or self.isVertical()
    
    def isHorizontal(self):
        return self.start.y == self.end.y
    
    def isVertical(self):
        return self.start.x == self.end.x

    def print(self):
        return self.start.print() + ' -> ' + self.end.print() 
   
    def getStraightPoints(self):
        points = []
        if(self.isHorizontal()):
            start = min(self.start.x,self.end.x)
            end = max(self.start.x,self.end.x)
            while start <= end:
                points.append(Vector(start,self.start.y))
                start += 1
        else:
            start = min(self.start.y,self.end.y)
            end = max(self.start.y,self.end.y)
            while start <= end:
                points.append(Vector(self.start.x,start))
                start += 1
        return points

    def getDiagonalPoints(self):
        points = []
        if self.isHorizontal() == False and self.isVertical() == False:
            slope = (self.end.y - self.start.y) / (self.end.x - self.start.x)
            offset = self.start.y - self.start.x * slope 
            

            start = min(self.start.x,self.end.x)
            end = max(self.start.x,self.end.x)
            while start <= end:
                 points.append(Vector(start,start*slope+offset))
                 start += 1
        
        return points
    

    def getY(self,x):
        if self.isHorizontal():
            return self.start.y
        if self.isVertical():
            return False
        
        # slope = (self.end.y - self.start.y) / (self.end.y
    def getX(self,y):
        if self.isVertical():
            return self.start.x
        if self.isHorizontal():
            return False
        
class Map:
    def __init__(self):
        self.rows = []
        self.points = []
    def addPoints(self,linePoints):
        for point in linePoints:
            self.addPoint(point)
            
    def addPoint(self,point):
        while len(self.points) <= point.x:
            self.points.append([])
        
        while len(self.points[point.x]) <= point.y:
            self.points[point.x].append(0)
        
        self.points[point.x][point.y] += 1
        
    def doublePointCount(self):
        

        multiplecount = 0;
        for x,row in enumerate(self.points):
            for count in row:
                if(count > 1):
                    multiplecount += 1
                
        print(multiplecount)


part_one('test.txt')
part_one('real.txt')
part_two('test.txt')
part_two('real.txt')