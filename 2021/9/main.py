from enum import unique
import re
import statistics

def part_one(file):
    map = read_file(file)
    
    count = 0
    lowPoints = map.findLowPoints()
    for point in lowPoints:
        count += point.val + 1

    print('P1 ' + file + ': ' + str(count))
    
    
def part_two(file):
    map = read_file(file)

    lowPoints = map.findLowPoints()
    basinSizes = []
    for point in lowPoints:
        basinSizes.append(len(point.getBasin([])))
    
    basinSizes.sort(reverse=True)

    solution = basinSizes[0]*basinSizes[1]*basinSizes[2]    
    
    print('P2 ' + file + ': ' + str(solution))


def read_file(file):
    file_contents = open("./input/" + file, "r").read().splitlines()
    rows = []
    map = Map()
    
    for row,cols in enumerate(file_contents):
        for col,number in enumerate(cols):
            map.addPoint(Point(col,row,int(number)))
    return map
    
class Map:
    def __init__(self):
        self.rows = []
    
    def addPoint(self, point):
        while point.x >= len(self.rows):
            self.rows.append([])
        while point.y >= len(self.rows[point.x]):
            self.rows[point.x].append([])
        self.rows[point.x][point.y] = point

        if(point.x > 0):
            point.linkLeft(self.rows[point.x-1][point.y])
        if(point.y > 0):
            point.linkTop(self.rows[point.x][point.y-1])
        
    def findLowPoints(self):
        lowPoints = []
        for cols in self.rows:
            for point in cols:
                if point.isLowPoint():
                    lowPoints.append(point)
        return lowPoints
    
    
class Point:
    def __init__(self,x,y,val):
        self.x = x
        self.y = y
        self.val = int(val)
        self.top = False
        self.left = False
        self.bottom = False
        self.right = False
    
    def linkLeft(self,other):
        self.left = other
        other.right = self
    
    def linkTop(self,other):
        self.top = other
        other.bottom = self
    
    def isLowPoint(self):
        return (
            (self.top == False or self.top.val > self.val)
            and (self.left == False or self.left.val > self.val)
            and (self.bottom == False or self.bottom.val > self.val)
            and (self.right == False or self.right.val > self.val)
        )

    def getBasin(self, points):
        if self in points:
            return
        if self.val > 8:
            return
        points.append(self)
        if self.top:
            self.top.getBasin(points)
        if self.bottom:
            self.bottom.getBasin(points)
        if self.left:
            self.left.getBasin(points)
        if self.right:
            self.right.getBasin(points)
        
        return points


part_one('test.txt')
part_one('real.txt')
part_two('test.txt')
part_two('real.txt')
