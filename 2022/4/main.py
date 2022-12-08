from enum import unique
from fractions import Fraction
import re
import statistics

def part_one(file):
    data = read_file(file)
    count = 0
    for pair in data:
        if (pair[0][0] >= pair[1][0] and pair[0][1] <= pair[1][1]) or (pair[0][0] <= pair[1][0] and pair[0][1] >= pair[1][1]):
            count += 1
    
    print(count)

def part_two(file):
    data = read_file(file)
    count = 0
    for pair in data:
        if (pair[1][0] <= pair[0][0] <= pair[1][1]) or (pair[1][0] <= pair[0][1] <= pair[1][1]) or (pair[0][0] <= pair[1][0] <= pair[0][1]) :
            count += 1
    print(count)

    

def read_file(file):
    lines = open("./input/" + file, "r").read().splitlines()
    data = []
    for line in lines:
        pairs = line.split(',')
        a = pairs[0].split('-')
        b = pairs[1].split('-')
        dataLine = [[int(a[0]),int(a[1])],[int(b[0]),int(b[1])]]
        data.append(dataLine)
    return data

part_one('test.txt')
part_one('real.txt')
part_two('test.txt')
part_two('real.txt')
