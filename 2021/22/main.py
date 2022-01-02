from enum import unique
from fractions import Fraction
from os import stat
import re
import statistics

def part_one(file):
   
    lines = read_file(file)
    limitCube = Rectangle(False,Vector(-500,-500,-500),Vector(500,500,500))

    rectangles = []
    for line in lines:
        l = re.match('([a-z]+) x=(-{0,1}[0-9]+)\.+(-{0,1}[0-9]+),y=(-{0,1}[0-9]+)\.+(-{0,1}[0-9]+),z=(-{0,1}[0-9]+)\.+(-{0,1}[0-9]+)',line)
        
        r = Rectangle(l[1] == 'on', Vector(l[2],l[4],l[6]),Vector(l[3],l[5],l[7]))
        r.max.x += 1
        r.max.y += 1
        r.max.z += 1
        
        if not r.intersects(limitCube):
            continue
        
        if r.state:
            addToListWithoutOverlap(rectangles,r)
            a = len(rectangles)

            # if getListOverlapCount(rectangles) > 0:
                # print('exiting with overlap')
                # return
            # cleanupOverlap(rectangles)
            # print('oc',a-len(rectangles) )
        else:
            for existingR in rectangles[:]:
                if existingR.intersects(r):
                    rectangles.remove(existingR)
                    rectangles += existingR.clipOutRectangle(r)
    
   
    Rectangle.combineRectangles(rectangles)
    
    answer = 0
    for r in rectangles:
        # print(r)
        answer += r.getPointsCount() 
    print('P1 ' + file + ': ' + str(answer))
    
    
def part_two(file):
    lines = read_file(file)
    
    rectangles = []
    
    count = 0
    for line in lines:
        l = re.match('([a-z]+) x=(-{0,1}[0-9]+)\.+(-{0,1}[0-9]+),y=(-{0,1}[0-9]+)\.+(-{0,1}[0-9]+),z=(-{0,1}[0-9]+)\.+(-{0,1}[0-9]+)',line)
        
        r = Rectangle(l[1] == 'on', Vector(l[2],l[4],l[6]),Vector(l[3],l[5],l[7]))
        r.max.x += 1
        r.max.y += 1
        r.max.z += 1
        
        if r.state:
            addToListWithoutOverlap(rectangles,r)
            a = len(rectangles)

            # if getListOverlapCount(rectangles) > 0:
            #     print('exiting with overlap')
            #     return
            # cleanupOverlap(rectangles)
            # print('oc',a-len(rectangles) )
        else:
            for existingR in rectangles[:]:
                if existingR.intersects(r):
                    rectangles.remove(existingR)
                    rectangles += existingR.clipOutRectangle(r)
        count +=1
        # print(count/len(lines))
   
    Rectangle.combineRectangles(rectangles)
    
    answer = 0
    for r in rectangles:
        answer += r.getPointsCount() 
    print('P2 ' + file + ': ' + str(answer))


def read_file(file):
    file_contents = open("./input/" + file, "r").read().splitlines()
    
    return file_contents

# def cleanupOverlap(rectangles):
#     overlap = True
#     while overlap:
#         overlap = False
#         for r in rectangles[:]:
#             if r not in rectangles:
#                 continue

#             overlapsWith = next((x for x in rectangles if x != r and x.intersects(r)), False)
#             if not overlapsWith:
#                 continue
#             overlap = True
            
#             rectangles.remove(r)
#             rectangles.remove(overlapsWith)
#             rectangles += r.mergeWithRectangle(overlapsWith)




def clipRectangleOutOfList(rectangleToCLipOut, rectangles):
    clippedRectangles = []
    for r in rectangles:
        clippedRectangles += r.clipOutRectangle(rectangleToCLipOut)
    Rectangle.combineRectangles(clippedRectangles)
    return clippedRectangles

def addToListWithoutOverlap(rectangles,rectangleToAdd):
    # We have one (long list) of rectangles, that do not overlap
    # We have one rectangle that may overlap with one or more rectangles in the big list
    # We want to end upt with a collection of rectangles that overlap in no way with
    # the rectangles in the big list.

    overlapsWith = list(filter(lambda ro: ro.intersects(rectangleToAdd),rectangles))
    rectanglesToAdd = [rectangleToAdd]
    for ro in overlapsWith:
        rectanglesToAdd = clipRectangleOutOfList(ro,rectanglesToAdd)

    Rectangle.combineRectangles(rectanglesToAdd)

    rectangles += rectanglesToAdd


class Rectangle:

    def __init__(self,state,pMin,pMax):
         self.state = state
         self.min = pMin
         self.max = pMax
    
    def __str__(self):

        state = 'on'
        if not self.state:
            state = 'off'

        return 'rect + ' + state + ' (' + str(self.min) + ') - (' + str(self.max) + ')'

    def intersects(self,other):
        if (
            self.max.x <= other.min.x or
            self.max.y <= other.min.y or
            self.max.z <= other.min.z or
            other.max.x <= self.min.x or
            other.max.y <= self.min.y or
            other.max.z <= self.min.z
        ):
            return False
        
        return True
    
    def mergeWithRectangle(self,other):
        # Assuming there is an intersect we want to cut up this rectangle.
        # The resulting rectangles should make up the original rectangle except for the points
        # that should be turned off
        
        rectangles = self.splitRectangles(other)

        Rectangle.combineRectangles(rectangles)
        
        return rectangles
        
        
    def combineRectangles(rectangles):
        merges = 1
        while merges > 0:
            startCount = len(rectangles)
            for r in rectangles[:]:
                if r not in rectangles:
                    continue
                mergeWith = next((x for x in rectangles if x.canBeCombinedWith(r)), False)
                if mergeWith:
                    
                    combInfo = r.canBeCombinedWith(mergeWith)
                    axis = combInfo[0]
                    
                    if combInfo[1] == 'min':
                        r.min.setVal(axis,mergeWith.min.getVal(axis))
                    else:
                        r.max.setVal(axis,mergeWith.max.getVal(axis))
                        
                    rectangles.remove(mergeWith)
            merges = startCount - len(rectangles)

    def canBeCombinedWith(self,other):
        eqX = (self.min.x == other.min.x and self.max.x == other.max.x)
        eqY = (self.min.y == other.min.y and self.max.y == other.max.y)
        eqZ = (self.min.z == other.min.z and self.max.z == other.max.z)

        if eqX and eqY:
            if self.min.z == other.max.z:
                return ['z','min']
            if self.max.z == other.min.z:
                return ['z','max']
        
        if eqX and eqZ:
            if self.min.y == other.max.y:
                return ['y','min']
            if self.max.y == other.min.y:
                return ['y','max']
        
        if eqY and eqZ:
            if self.min.x == other.max.x:
                return ['x','min']
            if self.max.x == other.min.x:
                return ['x','max']
        
        return False

    
    def clipOutRectangle(self,other):
        rectangles = self.splitRectangles(other)
        for r in rectangles[:]:
            if r.intersects(other):
                rectangles.remove(r)

        Rectangle.combineRectangles(rectangles)

        return rectangles
        

    def splitRectangles(self,other):
        
        allPlanes = [
            [self.min.x,self.max.x,other.min.x,other.max.x],
            [self.min.y,self.max.y,other.min.y,other.max.y],
            [self.min.z,self.max.z,other.min.z,other.max.z]
        ]
        
        rectangles = [self,other]        
        for i,planes in enumerate(allPlanes):
            planes.sort()
            dim = 'x'
            if i == 1:
                dim = 'y'
            if i == 2:
                dim = 'z'
         
            for plane in planes:
                for r in rectangles[:]:
                    newRectangles = r.splitOnPlane(dim,plane)
                    if newRectangles:
                        rectangles.remove(r)
                        rectangles += newRectangles


        return Rectangle.removeDoubles(rectangles)

    def removeDoubles(rectangles):
        noDoubles = []
        for r in rectangles:
            if len(list(filter(lambda dr: dr.eq(r) ,noDoubles ))) == 0:
                noDoubles.append(r)

        return noDoubles

    def splitOnPlane(self, dim, plane):
        if self.min.getVal(dim) >= plane or self.max.getVal(dim) <= plane:
            return False

        r1 = self.copy()
        r1.max.setVal(dim,plane)
        r2 = self.copy()
        r2.min.setVal(dim,plane)
        return[r1,r2]


    def copy(self):
        return Rectangle(self.state,self.min.copy(),self.max.copy())

    def eq(self,other):
        return self.min.eq(other.min) and self.max.eq(other.max)

    def getPoints(self):
        points = []
        for x in range(self.min.x,self.max.x):
            for y in range(self.min.y,self.max.y):
                for z in range(self.min.z,self.max.z):
                    points.append(Vector(x,y,z))
        return points

    def getPointsCount(self):
        total = 1
        for axis in ['x','y','z']:
            total *= (self.max.getVal(axis) - self.min.getVal(axis))
        return total

class Vector:
    def __init__(self,x,y,z):
        self.x = int(x)
        self.y = int(y)
        self.z = int(z)
    def __str__(self):
        return str(self.x) + ',' + str(self.y) + ',' + str(self.z)

    def copy(self):
        return Vector(self.x,self.y,self.z)

    def setVal(self,dim,val):
        if dim == 'x':
            self.x = val
        if dim == 'y':
            self.y = val
        if dim == 'z':
            self.z = val

    def getVal(self,dim):
        if dim == 'x':
            return self.x
        if dim == 'y':
            return self.y
        if dim == 'z':
            return self.z
        return False
    
    def eq(self,other):
        return self.x == other.x and self.y == other.y and self.z == other.z


part_one('test0.txt')
part_one('test.txt')
part_one('real.txt')
part_two('test2.txt')
part_two('real.txt')
