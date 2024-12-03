import re
import math
from typing import ChainMap
from dataline import DataLine

varationsCache = {}

def part_one(file):
    lines = read_file(file)
    
    total = 0
    for line in lines:
        dataL = DataLine(line)
        total += dataL.total

    return print('P1 - ' + file + ': ' + str(total))

def part_two(file):
    lines = read_file(file)
    total = 0

    for line in lines:
        parts = line.split(' ')
        mapParts = []
        numberParts = []
        while len(mapParts) < 5:
            mapParts.append(parts[0])
            numberParts.append(parts[1])
        nLine = '?'.join(mapParts) + ' ' + ','.join(numberParts)
        
        dataL = DataLine(nLine)
        total += dataL.total


    return print('P2 - ' + file + ': ' + str(total))

def read_file(file):
    lines = open("./input/" + file, "r").read().splitlines()
        
    return lines

part_one('test.txt')
part_one('real.txt')

part_two('test.txt')
# part_two('real.txt')

        

# data = parseData(getDayOneTest())