from enum import unique
import re
import statistics

def part_one(file):
    (stacks,instructions) = read_file(file)
    followInstructions(stacks,instructions)
    
    
def part_two(file):
    (stacks,instructions) = read_file(file)
    followInstructions(stacks,instructions,True)
    
def read_file(file):
    
    lines = open("./input/" + file, "r").read().splitlines()
    rows = lines[0:lines.index('') -1]
    rows.reverse()
    numbers = lines[lines.index('') -1]
    stacks = []

    i = 0
    for number in numbers:
        if number != ' ':
            stack = ''
            for row in rows:
                if row[i] != ' ':
                    stack += row[i]
                
            stacks.append(stack)
        i += 1

    instructions = list(map(lambda x: re.findall('(\d+)', x), lines[lines.index('') +1:]))

    return (stacks,instructions)

def parseInstruction(instruction):
    return 
    
def followInstructions(stacks,instructions,pickMultiple = False):
    for i in instructions:
        size = int(i[0])
        fromStack = int(i[1])-1
        toStack = int(i[2])-1
        if pickMultiple:
            stacks[toStack] += stacks[fromStack][-1*size:]
        else:
            stacks[toStack] += stacks[fromStack][-1*size:][::-1]
        stacks[fromStack] = stacks[fromStack][0:-1*size]
    result = ''
    for s in stacks:
        result += s[-1]
    print(result)

    
part_one('test.txt')
part_one('real.txt')
part_two('test.txt')
part_two('real.txt')