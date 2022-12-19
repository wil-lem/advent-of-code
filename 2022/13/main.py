from enum import unique
from fractions import Fraction
import re
import statistics
import math

def part_one(file):
    pairs = read_file(file)
    count = 0
    for i,pair in enumerate(pairs):
        if comparePair(pair[0],pair[1]) > 0:
            count += i+1
    print(count)

def part_two(file): 
    pairs = read_file(file)
    pairs.append([[[2]],[[6]]])

    singles = []
    for pair in pairs:
        for item in pair:
            added = False
            for i,sortedItem in enumerate(singles):
                if comparePair(sortedItem,item) < 0:
                    singles = singles[0:i] + [item] + singles[i:]  
                    added = True
                    break
            if added == False:
                singles.append(item)

        a = -1
        i = 0

    decoder = 1
    for i,single in enumerate(singles):
        if str(single) in ['[[2]]','[[6]]']:
            decoder *= i+1
    
    print(decoder)

def read_file(file):
    lines = open("./input/" + file, "r").read().splitlines()
    pairs = []
    for i in range(0,int((len(lines)+1)/3)):
        pairs.append([eval(lines[i*3]),eval(lines[i*3+1])])
    
    return pairs


def comparePair(leftPart,rightPart):
    if isinstance(leftPart,list) and isinstance(rightPart,list):
        return compareLists(leftPart,rightPart)
    if isinstance(leftPart,int) and isinstance(rightPart,int):
        return rightPart - leftPart
    if isinstance(leftPart,int):
        return compareLists([leftPart],rightPart)
    return compareLists(leftPart,[rightPart])

def compareLists(leftList, rightList):
    # print('compart list',leftList,rightList)
    for i,item in enumerate(leftList):
        if len(rightList) < i + 1:
            return -1
        result = comparePair(item,rightList[i])
        # print('c',i,result,item,rightList[i])
        if result != 0:
            return result
    if len(leftList) == len(rightList):
        return 0
    return 1
    # print('0',leftPart)    
    # print('1',rightPart)
    # print('left int',isinstance(leftPart,int))

    # print('left list',isinstance(leftPart,list))

    # isinstance(x, int)
part_one('test.txt')
part_one('real.txt')
part_two('test.txt')
part_two('real.txt')
