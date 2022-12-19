from enum import unique
from fractions import Fraction
import re
import statistics
import math

def part_one(file):
    points = read_file(file)
    
    currentPoints = list(filter(lambda point: point.start,points))
    endPoint = list(filter(lambda point: point.stop,points))[0]
    steps = 0
    
    while endPoint not in currentPoints:
        connectedPoints = []
        for point in currentPoints:
            point.distance = steps
            for unVisitedPoint in point.getUnvisited():
                if unVisitedPoint not in connectedPoints:
                    connectedPoints.append(unVisitedPoint)
        currentPoints = connectedPoints
        steps += 1
    
    print(steps)

def part_two(file): 
    points = read_file(file)
    
    
    currentPoints = list(filter(lambda point: point.elevation == 1,points))
    endPoint = list(filter(lambda point: point.stop,points))[0]
    steps = 0
    
    while endPoint not in currentPoints:
        connectedPoints = []
        for point in currentPoints:
            point.distance = steps
            for unVisitedPoint in point.getUnvisited():
                if unVisitedPoint not in connectedPoints:
                    connectedPoints.append(unVisitedPoint)
        currentPoints = connectedPoints
        steps += 1
    
    print(steps)

def read_file(file):
    lines = open("./input/" + file, "r").read().splitlines()
    
    map = []
    points = []
    for y,line in enumerate(lines):
        row = []
        for x,letter in enumerate(line):
            row.append(Point(letter))
            if x > 0:
                row[x].connect(row[x-1])
            if y > 0:
                row[x].connect(map[y-1][x])
            points.append(row[x]) 
        map.append(row)
    return points

class Point:
    def __init__(self,letter) -> None:
        
        self.start = False
        self.stop = False
        
        if letter == 'S':
            self.start = True
            letter = 'a'
        if letter == 'E':
            self.stop = True
            letter = 'z'

        self.elevation = ord(letter) - 96
        self.distance = -1

        self.top = False
        self.bottom = False
        self.right = False
        self.left = False
        
        self.connected = []
        pass
    
    def connect(self,other):
        if self.elevation >= other.elevation -1:
            self.connected.append(other)
        if other.elevation >= self.elevation -1:
            other.connected.append(self)
        
    def getUnvisited(self):
        return list(filter(lambda connectedPoint: connectedPoint.distance < 0, self.connected))

    def getUnvisitedOrCloser(self,distance):
        return list(filter(lambda connectedPoint: connectedPoint.distance < 0 or connectedPoint.distance > 0, self.connected))
    


part_one('test.txt')
part_one('real.txt')
part_two('test.txt')
part_two('real.txt')
