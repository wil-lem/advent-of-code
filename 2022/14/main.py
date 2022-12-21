from enum import unique
from fractions import Fraction
import re
import statistics
import math
import time
import os


def part_one(file):
    caveLines = read_file(file)
    
    # caveLines = [[[10,10],[12,10],[12,12]]]
    sandStart = [500,0]
    (minC,maxC) = getMinMax(caveLines)

    sandStart[0] -= minC[0]
    minC[1] = min(minC[1],sandStart[1])
    
    # minC = [1,1]
    # maxC = [2,2]
    caveMap = buildEmptyCave(minC,maxC,0)
    fillCave(caveLines,caveMap,minC,0)

    count = dropSand(caveMap,sandStart)

    print(count)
    
def part_two(file): 
    caveLines = read_file(file)
    
    # caveLines = [[[10,10],[12,10],[12,12]]]
    sandStart = [500,0]
    (minC,maxC) = getMinMax(caveLines)
    print(maxC)
    print(sandStart)
    floor = [[sandStart[0] - maxC[1] - 3, maxC[1]+2],[sandStart[0] + maxC[1] + 3 ,maxC[1]+2]]
    caveLines.append(floor)
    
    (minC,maxC) = getMinMax(caveLines)
    


    sandStart[0] -= minC[0]
    minC[1] = min(minC[1],sandStart[1])
    
    # # minC = [1,1]
    # # maxC = [2,2]
    caveMap = buildEmptyCave(minC,maxC,0)
    fillCave(caveLines,caveMap,minC,0)

    printCave(caveMap,0,30)
    count = dropSand(caveMap,sandStart)

    # print(count)



def dropSand(caveMap,sandStart):
    
    voidReached = False
    count = 0
    maxRow = 0
    while not voidReached:
        grain = sandStart[:]

        moved = True
        while moved:
            
            if grain[1]+1 == len(caveMap):
                moved = False
                voidReached = True
                continue

            if caveMap[grain[1]+1][grain[0]] < 1:
                grain[1] += 1
                continue
            
            
            # if grain[0]-1 == 0:
            #     moved = False
            #     voidReached = True
            #     continue
            
            if caveMap[grain[1]+1][grain[0]-1] < 1:
                grain[1] += 1
                grain[0] -= 1
                continue

            # if grain[0]+1 == len(caveMap[0]):
            #     moved = False
            #     voidReached = True
            #     continue
            
            if caveMap[grain[1]+1][grain[0]+1] < 1:
                grain[1] += 1
                grain[0] += 1
                continue

            moved = False
            caveMap[grain[1]][grain[0]] = 2
            count += 1
            
            if grain[0] == sandStart[0] and grain[1] == sandStart[1]:
                print('plugged hole')
                print(count)
                voidReached = True
                continue

            # os.system('clear')
            # maxRow = max(maxRow,grain[1])
            # printCave(caveMap,maxRow,30)
            # time.sleep(.01)

    return count

def fillCave(caveLines,map,minC,padding):
    for caveLine in caveLines:
        for i in range(0,len(caveLine)-1):
            startC = caveLine[i]
            endC = caveLine[i+1]

            dimension = 0
            other = 1

            if startC[0] == endC[0]:
                dimension = 1
                other = 0

            startVal = min(startC[dimension],endC[dimension])
            endVal = max(startC[dimension],endC[dimension])
            
            for j in range(startVal,endVal+1):
                if dimension == 1:
                    map[j+padding-minC[1]][startC[0]-minC[0]] = 1
                else:
                    map[startC[1]+padding-minC[1]][j-minC[0]] = 1

def printCave(caveMap, maxRow,length):
    maxRow = max(maxRow-length,0)

    for y in caveMap[maxRow:maxRow+length]:
        line = ''
        for x in y:
            symbol = '.'
            if x == 1:
                symbol = '#'
            if x == 2:
                symbol = 'o'
            line += symbol
        print(line)  

def buildEmptyCave(minC,maxC,padding=0):
    caveMap = []
    caveRow = []
    for x in range(minC[0]-padding,maxC[0]+1+padding):
        caveRow.append(0)
    for y in range(minC[1]-padding, maxC[1]+1+padding):
        caveMap.append(caveRow[:])
    return caveMap

def read_file(file):
    caveMap = []
    lines = open("./input/" + file, "r").read().splitlines()

    #First prepare all the data
    rockLines = []
    for line in lines:
        rockLine = []
        for coord in line.split(' -> '):
            coordInt = list(map(lambda x: int(x),coord.split(',')))
            rockLine.append(coordInt)
                
        rockLines.append(rockLine)

    return rockLines


def getMinMax(rockLines):
    minCoord = [-1,-1]
    maxCoord = [-1,-1]

    for line in rockLines:
        for coord in line:
            if minCoord[0] < 0:
                minCoord = coord[:]
                maxCoord = coord[:]
            minCoord[0] = min(minCoord[0],coord[0])
            minCoord[1] = min(minCoord[1],coord[1])
            maxCoord[0] = max(maxCoord[0],coord[0])
            maxCoord[1] = max(maxCoord[1],coord[1])

    return (minCoord,maxCoord)


    for x in range(minCoord[0],maxCoord[0]+1):
        for y in range(minCoord[0],maxCoord[0]+1):
        
            print(x-minCoord[0])
    
    print(rockLines)
    print(minCoord)
    print(maxCoord)

    
            # rockLine.append(coordInt)
            # if len(rockLine) == 2:
            #     maxX = max(rockLine[0][0],rockLine[1][0])
            #     maxY = max(rockLine[0][1],rockLine[1][1])


            #     print(rockLine)
            #     rockLine.pop(0)


# part_one('test.txt')
# part_one('real.txt')
part_two('test.txt')
part_two('real.txt')
