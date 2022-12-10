from enum import unique
from fractions import Fraction
import re
import statistics
import math

def part_one(file):
    data = read_file(file)
    cycle = 0
    x = 1
    score = 0
    for line in data:
        op = line[0:4]
        mod = 0
        if op == 'addx':
            mod = int(line[5:])
            cycle +=1
            if (cycle+20) % 40 == 0:
                score += cycle * x

        cycle += 1
        if (cycle+20) % 40 == 0:
                score += cycle * x

        x += mod

    print(score)

def part_two(file): 
    data = read_file(file)
    print('')
    cycle = 0
    x = 1
    screenLine = ''
    for line in data:
        op = line[0:4]
        mod = 0
        if op == 'addx':
            mod = int(line[5:])
            screenLine += '#' if x-1 <= cycle%40 <= x+1 else '.'
            cycle +=1
            if (cycle) % 40 == 0:
                print(screenLine)
                screenLine = ''
        
        screenLine += '#' if x-1 <= cycle%40 <= x+1 else '.'
        cycle += 1
        if (cycle) % 40 == 0:
                print(screenLine)
                screenLine = ''
        x += mod
    
def read_file(file):
    return open("./input/" + file, "r").read().splitlines()



part_one('test.txt')
part_one('real.txt')
part_two('test.txt')
part_two('real.txt')
