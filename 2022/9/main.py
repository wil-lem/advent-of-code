from enum import unique
from fractions import Fraction
import re
import statistics
import math

def part_one(file):
    data = read_file(file)
    knots = [Vector(),Vector()]
    moveKnots(data,knots)
    

def part_two(file): 
    data = read_file(file)
    knots = []
    for i in range(0,10):
        knots.append(Vector())
    moveKnots(data,knots)
    
def moveKnots(data,knots):
    positions = []
    for i in data:
        (direction,amount) = i.split(' ')
        for j in range(0,int(amount)):
            for g,knot in enumerate(knots):
                if g==0:
                    knot.move(direction)
                    continue
                knot.moveTo(knots[g-1])
            
            if knots[-1].output() not in positions:
                positions.append(knots[-1].output())
    print(len(positions))

def read_file(file):

    return open("./input/" + file, "r").read().splitlines()


class Vector:
    def __init__(self) -> None:
        self.x = 0
        self.y = 0
        pass
    
    def output(self) -> str:
        return '(' + str(self.x) + ',' + str(self.y) +')'
    
    def move(self,direction):
        check = self.output() + ' '
        mod = 1 if direction in ['U','R'] else -1
        axis = 'y' if direction in ['U','D'] else 'x'
        setattr(self,axis,getattr(self,axis)+mod)
    
    def moveTo(self,other):
        diff = self.sub(other)
        distance = self.distance(other)
        if distance > math.sqrt(2):
            if diff.x != 0:
                self.x += 1 if self.x < other.x else -1
            if diff.y != 0:
                self.y += 1 if self.y < other.y else -1
                
    def distance(self,other):
        diff=self.sub(other)
        return math.sqrt(pow(diff.x,2)+pow(diff.y,2))

    def sub(self,other):
        result = Vector()
        result.x = self.x - other.x
        result.y = self.y - other.y
        return result


part_one('test.txt')
part_one('real.txt')
part_two('test.txt')
part_two('test2.txt')
part_two('real.txt')
