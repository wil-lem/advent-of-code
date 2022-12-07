from enum import unique
from fractions import Fraction
import re
import statistics

def part_one(file):
    print(getMarkerIndex(open("./input/" + file, "r").read(),4))
        
def part_two(file): 
    print(getMarkerIndex(open("./input/" + file, "r").read(),14))
    
def read_file(file):
    return 

def getMarkerIndex(data,markerLength):
    part = ''
    for i,letter in enumerate(data):
        prev = part.find(letter)
        if prev > -1:
            part = part[prev+1:]
        part += letter
        if len(part) == markerLength:
            return i + 1



part_one('test.txt')
part_one('real.txt')
part_two('test.txt')
part_two('real.txt')
