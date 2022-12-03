from enum import unique
from fractions import Fraction
import re
import statistics

def part_one(file):
    data = read_file(file)
    score = 0
    for i in data:

        compartments = [ i[0:int(len(i)/2)], i[int(len(i)/2):] ]
        for letter in compartments[0]:
            if compartments[1].find(letter) > -1:            
                shared = letter
        score += getPrio(shared)
    print(score)

def part_two(file):
    data = read_file(file)
    score = 0 
    
    group = []
    for i in data:
        if len(group) > 1:
            match = ''
            for letter in i:
                if match == '' and group[0].find(letter) > -1 and group[1].find(letter) > -1:
                    match = letter
            score += getPrio(match)
            group = []
        else:
            group.append(i)
    print(score)

def read_file(file):
    return open("./input/" + file, "r").read().splitlines()
    
def getPrio(letter):
    prio = ord(letter) - 96
    if prio < 0:
        prio += 58
    return prio


part_one('test.txt')
part_one('real.txt')
part_two('test.txt')
part_two('real.txt')
