import re
from readFile import ReadFile

def parseFile(filename):
    rf = ReadFile(filename)
    lines = rf.getLines()
    orderingRules = []
    updates = []

    for line in lines:
        digits = re.findall(r'(\d+)',line)
        if  re.search(r'\|',line):
            orderingRules.append(digits)
        elif len(digits) > 0:
            updates.append(digits)
    return orderingRules, updates

def filterRules(orderingRules, update):
    return [rule for rule in orderingRules if rule[0] in update and rule[1] in update]

def validateUpdate(orderingRules, update):
    ruleCopy = filterRules(orderingRules, update)
    for number in update:
        secondElements = [rule for rule in ruleCopy if rule[1] == number]
        if len(secondElements) > 0:
            return False
        # Remove all rules that have the number as first element
        ruleCopy = [rule for rule in ruleCopy if rule[0] != number]
    return True

def one(filename):
    orderingRules, updates = parseFile(filename)
    total = 0

    for update in updates:
        if validateUpdate(orderingRules, update):
            total += int(update[len(update) // 2])

    print('Total:', total)
        
def two(filename):
    orderingRules, updates = parseFile(filename)
    total = 0

    for update in updates:
        if not validateUpdate(orderingRules, update):
            ruleCopy = filterRules(orderingRules, update)
            for number in update:
                onRight = [rule for rule in ruleCopy if rule[1] == number]
                onLeft = [rule for rule in ruleCopy if rule[0] == number]
                
                if(len(onRight) == len(onLeft)):
                    total += int(number)
            
    print('Total:', total)
    
one(ReadFile.testFile())
one(ReadFile.realFile())
two(ReadFile.testFile())
two(ReadFile.realFile())