from enum import unique
from fractions import Fraction
import re
import statistics
import math
import time
import os


def part_one(file,lineNo):
    sensors = read_file(file)
    beacons = []
    
    for sensor in sensors:
        if sensor.by == lineNo and sensor.bx not in beacons:
            beacons.append(sensor.bx)

    mergedCoverage = getMergedCoverage(sensors,lineNo)
    
    foundBeacons = 0
    for bx in beacons:
        for cr in mergedCoverage:
            if cr[1] >= bx >= cr[0]:
                foundBeacons += 1
    
    count = foundBeacons *-1
    for cr in mergedCoverage:
        count += cr[1] - cr[0] + 1
    print(count)

def part_two(file,maxLineNo): 
    sensors = read_file(file)
    
    for lineNo in range(0,maxLineNo):
        mergedCoverage = getMergedCoverage(sensors,lineNo)
        if len(mergedCoverage) > 1:
            x = mergedCoverage[0][1]+1
            y = lineNo
            print(x*4000000+lineNo)
            break
        # if(lineNo%100000 == 0):
        #     print(lineNo)
        
def getMergedCoverage(sensors,lineNo):
    
    coverage = []
    for sensor in sensors:
        sensorCoverage = sensor.getLineCoverage(lineNo)

        if sensorCoverage == False:
            continue
    
        for i,prev in enumerate(coverage):
            if prev == False:
                continue
            if prev[0] <= sensorCoverage[0]:
                if prev[1] >= sensorCoverage[1]:
                    # Completely inside other range
                    # We're done
                    sensorCoverage = []
                    break
                if prev[1] >= sensorCoverage[0]:
                    # Prev sticks out on the left
                    coverage[i] = False
                    sensorCoverage = [prev[0],sensorCoverage[1]]
                    continue
            else:
                if prev[1] <= sensorCoverage[1]:
                    # Prev is competly inside sensor coverage
                    coverage[i] = False
                    continue
                if prev[0] <= sensorCoverage[1]:
                    # Prev sticks out on right side
                    coverage[i] = False
                    sensorCoverage = [sensorCoverage[0],prev[1]]
                    continue
                # No intersection
        
        if len(sensorCoverage) > 0:
            coverage.append(sensorCoverage)    
        coverage = list(filter(lambda c: c != False,coverage))
        
    return coverage
    
def read_file(file):
    lines = open("./input/" + file, "r").read().splitlines()
    sensors = []
    for line in lines:
        a = re.findall(r'=(-{0,1}[0-9]+)',line)
        sensors.append(Sensor(a[0],a[1],a[2],a[3]))
    return sensors

    
class Sensor:
    def __init__(self,x,y,bx,by) -> None:
        self.x = int(x)
        self.y = int(y)
        self.bx = int(bx)
        self.by = int(by)
        self.coverage = abs(self.x-self.bx) + abs(self.y-self.by)
        self.first = self.y - self.coverage
        self.last = self.y + self.coverage

        self.lastLine = False
        self.lastRange = False
        pass

    def getLineCoverage(self,lineNo):
        if lineNo < self.first or lineNo > self.last:
            return False
        
        if self.lastRange:
            if lineNo <= self.y:
                self.lastRange[0] -= 1
                self.lastRange[1] += 1
            else:    
                self.lastRange[0] += 1
                self.lastRange[1] -= 1
        else:
            coverage = self.coverage - abs(lineNo - self.y)
            self.lastRange = [self.x-coverage,self.x+coverage]
        return self.lastRange

part_one('test.txt',10)
part_one('real.txt',2000000)
part_two('test.txt',20)
part_two('real.txt',4000000)
