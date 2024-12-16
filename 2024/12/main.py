import re
import time


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def nextTo(self, v):
        if self.x == v.x and self.y == v.y + 1:
            return True
        if self.x == v.x and self.y == v.y - 1:
            return True
        if self.x == v.x + 1 and self.y == v.y:
            return True
        if self.x == v.x - 1 and self.y == v.y:
            return True
        return False

    def __eq__(self, value):
        return self.x == value.x and self.y == value.y
    
    def __str__(self):
        return f'({self.x},{self.y})'

class Line:
    def __init__(self, v, mod, axis):
        self.start = v
        self.mod = mod
        self.axis = axis

    def getEnd(self):
        if self.axis == 'x':
            return Vector(self.start.x + self.mod, self.start.y)
        else:
            return Vector(self.start.x, self.start.y + self.mod)

    def __str__(self):
        direction_map = {
            (-1, 0): '←',  # Left
            (1, 0): '→',   # Right
            (0, -1): '↑',  # Up
            (0, 1): '↓'    # Down
        }
        direction = direction_map.get((self.mod, 0) if self.axis == 'x' else (0, self.mod), '?')
        return f'Line from {self.start} to {self.getEnd()} in direction {direction}'

class Group:
    def __init__(self, char, v):
        self.char = char
        self.members = []
        self.members.append(v)
    
    def nextTo(self, char, v):
            
        if self.char != char:
            return False
        for memberV in self.members:
            if v.nextTo(memberV):
                return True
            
        return False
    
    def fenceLength(self):
        fenceCount = 0
        for v in self.members:
            surrounding = [1, 1, 1, 1]
            for otherV in self.members:
                if otherV.x == v.x and otherV.y == v.y + 1:
                    surrounding[0] = 0
                if otherV.x == v.x and otherV.y == v.y - 1:
                    surrounding[1] = 0
                if otherV.x == v.x + 1 and otherV.y == v.y:
                    surrounding[2] = 0
                if otherV.x == v.x - 1 and otherV.y == v.y:
                    surrounding[3] = 0
            fenceCount += sum(surrounding)
        return fenceCount
    
    def fenceLength2(self):

        fenceParts = []
        for v in self.members:

            surrounding = [1,1,1,1]
            for otherV in self.members:
                if v.x == otherV.x and v.y == otherV.y + 1:
                    surrounding[0] = 0
                if v.x == otherV.x and v.y == otherV.y - 1:
                    surrounding[1] = 0
                if v.x == otherV.x + 1 and v.y == otherV.y:
                    surrounding[2] = 0
                if v.x == otherV.x - 1 and v.y == otherV.y:
                    surrounding[3] = 0

            if surrounding[0] == 1:
                fenceParts.append(Line(v, 1, 'x')) # Top
            if surrounding[1] == 1:
                fenceParts.append(Line(Vector(v.x+1,v.y+1), -1, 'x')) # Bottom
            if surrounding[2] == 1:
                fenceParts.append(Line(Vector(v.x,v.y+1), -1, 'y')) # Left
            if surrounding[3] == 1:
                fenceParts.append(Line(Vector(v.x+1,v.y), 1, 'y')) # Right

        # Now we we can "build" the fence
        totalLength = 0
        fences = []
        
        while len(fenceParts) > 0:
            # Just get the first part to start with
            currentPart = fenceParts.pop(0)
            # print('Start Part:', currentPart)
            currentFenceParts = [currentPart]

            while(len([part for part in fenceParts if part.start == currentPart.getEnd()]) > 0):
                currentPart = [part for part in fenceParts if part.start == currentPart.getEnd()][0]
                # print('Next Part:', currentPart)
                currentFenceParts.append(currentPart)
                fenceParts.remove(currentPart)
            
            if currentFenceParts[0].start != currentFenceParts[-1].getEnd():
                print('open fence')
            fences.append(currentFenceParts)


        for fence in fences:
            fenceLength = 0

            for i, part in enumerate(fence):
                if i == 0:
                    continue
                if part.axis != fence[i-1].axis:
                    fenceLength += 1
            if fence[0].axis != fence[-1].axis:
                fenceLength += 1

            totalLength += fenceLength
        return totalLength


def main(filename):
  
    lines = open('input/' + filename + '.txt').read().splitlines()
    
    groups = []
    last = ''
    for y in range(0, len(lines)):
        for x in range(0, len(lines[y])):
            v = Vector(x, y)
            char = lines[y][x]
            # lines[y][x] = '.'
            
            connectedGroups = []
            for group in groups:
                if group.nextTo(char, v):
                    connectedGroups.append(group)
            
            if len(connectedGroups) == 0:
                group = Group(char, v)
                groups.append(group)
            elif len(connectedGroups) == 1:
                connectedGroups[0].members.append(v)
            else:
                connectedGroups[0].members.append(v)
                for i in range(1, len(connectedGroups)):
                    connectedGroups[0].members += connectedGroups[i].members
                    groups.remove(connectedGroups[i])
                    
    total = 0
    for group in groups:
        total += group.fenceLength() * len(group.members)

    total2 = 0
    for group in groups:
        total2 += group.fenceLength2() * len(group.members)
    print('Total:', total)
    
    print('Total2:', total2)
main('test')
# main('test2')
# main('test3')
main('real')