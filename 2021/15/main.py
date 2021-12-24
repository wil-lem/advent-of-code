from enum import unique
from fractions import Fraction
import re
import statistics
import sys
print(sys.getrecursionlimit())
sys.setrecursionlimit(100000)

def part_one(file):
    map = read_file(file)
    distance = map.findShortestPath()
    print('P1 ' + file + ': ' + str(distance))

def part_two(file):
    map = read_file(file)
    map.enlarge(5,5)
    map.linkPoints()

    distance = map.findShortestPath()
    print('P2 ' + file + ': ' + str(distance))

def read_file(file):
    file_contents = open("./input/" + file, "r").read().splitlines()
    rows = []
    map = Map()
    
    for row,cols in enumerate(file_contents):
        for col,number in enumerate(cols):
            map.addPoint(Point(col,row,int(number)))
    map.linkPoints()
    return map
 
class Map:
    def __init__(self):
        self.rows = []
    
    def addPoint(self, point):
        while point.y >= len(self.rows):
            self.rows.append([])
        while point.x >= len(self.rows[point.y]):
            self.rows[point.y].append([])
        self.rows[point.y][point.x] = point

    def enlarge(self,xRep,yRep):
        self.enlargeX(xRep)
        self.enlargeY(yRep)
        
    def enlargeX(self,xRep):
        newRows = []
        for row in self.rows:
            newRow = []
            for i in range(0,xRep):
                for point in row:
                    newPoint = Point(point.x + len(row) * i,point.y,point.val + i)
                    newRow.append(newPoint)
                    if newPoint.val > 9:
                        newPoint.val -= 9
            newRows.append(newRow)
        self.rows = newRows
        
    def enlargeY(self,yRep):
        newRows = []
        for i in range(0,yRep):
            for row in self.rows:
                newRow = []
                for point in row:
                    newPoint = Point(point.x,point.y + len(self.rows) * i,point.val + i)
                    newRow.append(newPoint)
                    if newPoint.val > 9:
                        newPoint.val -= 9
                newRows.append(newRow)
        self.rows = newRows
        
    def linkPoints(self):
        for row in self.rows:
            for point in row:
                if point.x > 0:
                    point.linkW(self.rows[point.y][point.x - 1])
                
                if point.y > 0:
                    point.linkN(self.rows[point.y-1][point.x])
                
    def printMap(self):
        printRows = ['']*10
        for row in self.rows:
            rowString = ""
            for point in row:
                rowString += str(point.val)
            print(rowString)

    def findShortestPath(self):
        self.rows[0][0].distance = 0
        points = [self.rows[0][1],self.rows[1][0]]

        size = len(self.rows[0])*len(self.rows)
        count = 0
        distance = 0

        while len(points) > 0:
            # print(count/size)
            # print(points[0].getMinimalDistance() - distance)
            # count+=1
            
            #Since sort is pretty expensive, only do it if the first point would increase the distance
            if points[0].getMinimalDistance() - distance > 0:
                points.sort(key=lambda point: point.getMinimalDistance())
            newPoint = points[0]
            newPoint.setMinimalDistance()
            distance = newPoint.distance
            
            # If we reached bottom-right return the distance
            if newPoint.x + 1 == len(self.rows[0]) and newPoint.y + 1 == len(self.rows):
                return newPoint.distance

            # Update points collection
            points.remove(newPoint)
            for newConnectedPoint in newPoint.getConnectedWithoutDistance():
                if newConnectedPoint not in points:
                    points.append(newConnectedPoint)
            
        return False

class Point:
    def __init__(self,x,y,val):
        self.x = x
        self.y = y
        self.val = int(val)
        self.distance = -1

        self.d = {
            "s": False,
            "n": False,
            "e": False,
            "w": False
        }
    
    def linkW(self,other):
        self.d['w'] = other
        other.d['e'] = self
    
    def linkN(self,other):
        self.d['n'] = other
        other.d['s'] = self

    def getConnected(self):
        dims = ['n','s','e','w']
        connected = []
        for dim in dims:
            if self.d[dim]:
                connected.append(self.d[dim])
        return connected

    def hasDistance(self):
        return self.distance > -1

    def getConnectedWithoutDistance(self):
        return list(filter(lambda point: not point.hasDistance(),self.getConnected()))
        
    def getMinimalDistance(self):

        connected = self.getConnected()
        connected = list(filter(lambda point: point.hasDistance(),connected))
        
        minDistance = False
        for point in connected:
            distance = point.distance + self.val
            if minDistance == False or distance < minDistance:
                minDistance = distance

        return minDistance

    def setMinimalDistance(self):
        self.distance = self.getMinimalDistance()

            
            
    
part_one('test.txt')
part_one('real.txt')
part_two('test.txt')
part_two('real.txt')
