from enum import unique
from fractions import Fraction
import re
import statistics


def part_one(file):
    count = findResult(file,10)
    print('P1 ' + file + ': ' + str(count))

def part_two(file):
    count = findResult(file,40)        
    print('P2' + file + ': ' + str(count))


def findResult(file,turns):

    # Read the file
    data = read_file(file)
    
    rules = data[0]
    stepSize = 5
    
    # Let's say for each rule we will calculate what it looks like in 5 steps.
    # After that we can calculate the same for 10,20 and finally 40
    for ruleName in rules:
        rule = rules[ruleName]
        rule.getString(rules,stepSize)
    
    for ruleName in rules:
        rule = rules[ruleName]
        rule.setCounter(rules,turns/2,stepSize)
       
    base = data[1]
    doneTurns = 0
    while doneTurns < turns/2:
        base = applyRules(base,rules,stepSize)
        doneTurns += stepSize
    
    # We're halfway there, rather than moving through all steps again we can just go through what we have and get the lettercount
    # we know we'll end upt with

    baseCounter = LetterCounter(base,True)
    for i in range(0,len(base)-1):
        pattern = base[i:i+2]
        baseCounter.add(rules[pattern].letterC)
        
    return baseCounter.max() - baseCounter.min()



    # Now go through the letter pairs
    
    # Walk through all

    # We assume that the rules are all the variation we're going to get. Say we have 2 letters A and B
    # theoretically we would need four rules AA,AB,BA and BB but depending on the configuration BB might
    # not be a rule.
    # Every pair of letters will be 3 letters after 1 turn, 5 after 2, 9(3), 17(4)
    # 0:2
    # 1:3
    # 2:5
    # 3:9
    # 4:17
    # s * 

    # print(rules)
    # print(base)
    # Expand polymer all the while adding the results to the total
    # Substract lowest from highest and return reults

def getCounter(base,rules,steps):
    for i in range(0,len(base) - 1):
        pair = base[i:i+2]
        rule = rules[pair]
        



def printDiffs(base,rules):
    newBase = applyRules(base,rules)
    lastLetters = countLetters(base)
    newLetters = countLetters(newBase)
    diffs = {}
    
    print('----------')
    
    for letter in lastLetters:
        if letter in newLetters:
            diffs[letter] = lastLetters[letter]/newLetters[letter]
    print(diffs)

    print()
    print()

def countLetters(base):
    letters = {}
    for letter in base:
        if letter not in letters:
            letters[letter] = base.count(letter)
    return letters

def applyRules(base, rules,turns = 1):
    newBase = base[0:1]
    for i in range(0,len(base)-1):
        pattern = base[i:i+2]
        insert = rules[pattern].counts[turns]
        newBase += insert[1:-1] + pattern[1:]
    return newBase

class Rule:
    def __init__(self,base,insert) -> None:
        self.base = base
        self.insert = insert
        self.counts = {}
        self.counts[1] = base[0:1] + insert + base[1:]
        self.letterC = {}
        pass

    def getString(self,rules,turns):
        if turns in self.counts:
            return self.counts[turns]
        
        prev = self.getString(rules,turns -1)
        next = applyRules(prev,rules)
        self.counts[turns] = next
        return next
    
    # Set a counter object for this rule, representing the letter count this rule will result in after the
    # number of turns.
    def setCounter(self,rules,turns,stepSize):
        doneTurns = 0
        base = self.base
        while doneTurns < turns:
            base = applyRules(base,rules,stepSize)
            doneTurns += stepSize
        self.letterC = LetterCounter(base)
        

class LetterCounter:
    def __init__(self,letters, includeSides=False) -> None:
        self.counts = {}
        if not includeSides:
            letters = letters[1:-1]

        for letter in letters:
            if letter in self.counts:
                self.counts[letter] = self.counts[letter] + 1
            else:
                self.counts[letter] = 1
        pass

    def __str__(self) -> str:
        letters = ''
        for letter in self.counts:
            letters += letter + ' (' + str(self.counts[letter]) + ') '
        return letters

    def min(self):
        return min(self.counts.values())
    
    def max(self):
        return max(self.counts.values())

    def add(self, other):
        for letter in other.counts:
            if letter in self.counts:
                self.counts[letter] += other.counts[letter]
            else:
                self.counts[letter] = other.counts[letter]
            

def expandRule(pattern,rules,count):
    rule = rules[pattern]
    newString = pattern[0:1] + rule['replace'] + pattern[-1]
    rule['counts'].append({'string':newString})


def read_file(file):
    file_contents = open("./input/" + file, "r").read().splitlines()
    rules = {}
    inputString = file_contents[0]
    for rule in file_contents[2:]:
        r = Rule(rule[0:2],rule[-1])
        rules[r.base] = r
    
    return rules,inputString

    
part_one('test.txt')
part_one('real.txt')
part_two('test.txt')
part_two('real.txt')
