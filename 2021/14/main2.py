from enum import unique
from fractions import Fraction
import re
import statistics

from yaml import dump


def part_one(file):
    count = findResult(file,10)
    print('P1 ' + file + ': ' + str(count))

def part_two(file):
    count = findResult(file,40)        
    print('P2 ' + file + ': ' + str(count))


def findResult(file,turns):

    # Read the file
    data = read_file(file)
    
    rules = data[0]
    base = data[1]

    doubles = {}

    for i in range(0,len(base) - 1):
        pair = base[i:i+2]
        
        rule = rules[pair]
        rule.count += 1

        if i > 0:
            doubleLetter = base[i:i+1]
            setOrIncrease(doubles,doubleLetter)
    
    for i in range(0,turns):
        for ruleBase in rules:
            rules[ruleBase].apply(doubles,rules)
        for ruleBase in rules:
            rules[ruleBase].applyCounts()
    
    # Sum it all up
    letterCounts = {}
    for rule in rules:
        rules[rule].addCounts(letterCounts)

    for letter in doubles:
        letterCounts[letter] -= doubles[letter]
    listCounts = letterCounts.values()
    
    return max(listCounts) - min(listCounts)

def setOrIncrease(dictObj,dictKey,value=1):
    if dictKey in dictObj:
        dictObj[dictKey] += value
    else:
        dictObj[dictKey] = value
    
def read_file(file):
    file_contents = open("./input/" + file, "r").read().splitlines()
    rules = {}
    inputString = file_contents[0]
    for rule in file_contents[2:]:
        r = Rule(rule[0:2],rule[-1])
        rules[r.base] = r
    
    return rules,inputString


class Rule:
    def __init__(self,base,insert) -> None:
        self.base = base
        self.insert = insert

        self.count = 0
        self.newCount = 0
        pass
    
    def addCounts(self,counts):
        for letter in self.base:
            setOrIncrease(counts,letter,self.count)

    def apply(self,doubles,rules):
        rules[self.base[0:1]+self.insert].newCount += self.count
        rules[self.insert+self.base[1:]].newCount += self.count

        setOrIncrease(doubles,self.insert,self.count)
        
    
    def applyCounts(self):
        self.count = self.newCount
        self.newCount = 0
    
part_one('test.txt')
part_one('real.txt')
part_two('test.txt')
part_two('real.txt')

