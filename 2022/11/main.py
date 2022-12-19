from enum import unique
from fractions import Fraction
import re
import statistics
import math

def part_one(file):
    monkeys = read_file(file)
    
    for round in range(0,20):
        for monkey in monkeys:
            while len(monkey.items) > 0:
                monkey.inspectedCount += 1
                item = monkey.items.pop(0)
                old = item.worry
                item.worry = eval(monkey.operation)
                
                item.worry = math.floor(item.worry/3)
                
                if item.worry%monkey.testDivision == 0:
                    monkeys[monkey.trueResult].items.append(item)
                else:
                    monkeys[monkey.falseResult].items.append(item)
    counts = list(map(lambda monkey: monkey.inspectedCount,monkeys))
    counts.sort()

    print(counts[-2]*counts[-1])

def part_two(file): 
    monkeys = read_file(file)
    divisionTotal = 1
    for monkey in monkeys:
        divisionTotal *= monkey.testDivision

    for round in range(0,10000):
        for monkey in monkeys:
            while len(monkey.items) > 0:
                monkey.inspectedCount += 1
                item = monkey.items.pop(0)
                old = item.worry
                item.worry = eval(monkey.operation)%divisionTotal
                
                if item.worry%monkey.testDivision == 0:
                    monkeys[monkey.trueResult].items.append(item)
                else:
                    monkeys[monkey.falseResult].items.append(item)

    counts = list(map(lambda monkey: monkey.inspectedCount,monkeys))
    counts.sort()

    print(counts[-2]*counts[-1])
    print(counts)

    
def read_file(file):
    data = open("./input/" + file, "r").read().splitlines()
    monkeys = [Monkey()]
    
    for line in data:
        if line == '':
            monkeys.append(Monkey())
        if line[11:16] == 'items':
            monkeys[-1].setItems(line[18:])  
        if line[2:11] == 'Operation':
            monkeys[-1].setOperation(line[18:])
        if line[2:6] == 'Test':
            monkeys[-1].setTestDivision(line[21:])
        if line[2:6] == 'Test':
            monkeys[-1].setTestDivision(line[21:])
        if line[4:11] == 'If true':
            monkeys[-1].setTrueResult(line[29:])
        if line[4:12] == 'If false':
            monkeys[-1].setFalseResult(line[30:])
    return monkeys

class Item:
    def __init__(self,worry) -> None:
        self.worry = worry
        
class Monkey:
    def __init__(self) -> None:
        self.items = []
        self.operation = False
        self.testDivision = False
        self.trueResult = False
        self.falseResult = False
        self.inspectedCount = 0
        
        pass

    def setOperation(self,line):
        self.operation = line

    def setTestDivision(self,line):
        self.testDivision = int(line)

    def setTrueResult(self,line):
        self.trueResult = int(line)

    def setFalseResult(self,line):
        self.falseResult = int(line)

    def setItems(self,items):
        for worry in map(lambda worry: int(worry),items.split(',')):
            self.items.append(Item(worry))

    

part_one('test.txt')
part_one('real.txt')
part_two('test.txt')
part_two('real.txt')
