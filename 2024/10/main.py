import re
import time
from readFile import ReadFile

def walkTrail(x,y,c,lines):
    endpoints = []
    for mod in [[-1,0],[1,0],[0,-1],[0,1]]:
        newX = x+mod[0]
        newY = y+mod[1]
        if newX < 0 or newX >= len(lines[0]):
            continue
        if newY < 0 or newY >= len(lines):
            continue
        nextC = int(lines[newY][newX])

        if c+1 == nextC:
            if nextC == 9:
                endpoints.append(str(newX) + '_' + str(newY))
                continue
            endpoints += walkTrail(newX,newY,nextC,lines)
    return endpoints
            
def main(filename):
    total = 0
    total2 = 0
    file = ReadFile(filename)
    lines = file.trimLines()
    for y,line in enumerate(lines):
        for x,char in enumerate(line):
            if char == '0':
                endpoints = walkTrail(x,y,int(char),lines)
                newEndPoints = []
                for point in endpoints:
                    if point not in newEndPoints:
                        newEndPoints.append(point)

                total += len(newEndPoints)
                total2 += len(endpoints)
                # total += score
    print(total)
    print(total2)

main(ReadFile.testFile())
main(ReadFile.realFile())