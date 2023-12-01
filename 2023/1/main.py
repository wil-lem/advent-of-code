import re
import math
from typing import ChainMap


def part_one(file):
    lines = read_file(file)
    total = 0
    for line in lines:
        first=''
        last=''
        for c in line:
            if c.isdigit():
                if first == '':
                    first = c
                last = c
        total += int(first+last)
    return print('P1 - ' + file + ': ' + str(total))

def part_two(file):
    lines = read_file(file)
    
    total = 0
    for line in lines:
        

        # for i,number in enumerate(numbers):
        #     line = line.replace(number,str(i+1))

        total += int(getLineFirstDigit(line) + getLineLastDigit(line))
    return print('P2 - ' + file + ': ' + str(total))

def getLineFirstDigit(line):
    for i,l in enumerate(line):
        if l.isdigit():
            return l
        wordValue = getWordValue(line[i:])
        if wordValue != '':
            return wordValue

def getLineLastDigit(line):
    for i,l in reversed(list(enumerate(line))):
        if l.isdigit():
            return l
        wordValue = getWordValue(line[i:])
        if wordValue != '':
            return wordValue
    return '1'

def getWordValue(line):
    numbers = ['one','two','three','four','five','six','seven','eight','nine']
    for i,word in enumerate(numbers):
        if word == line[0:len(word)]:
            return str(i+1)
    return ''

def getLineTotal(line):
    first=''
    last=''
    for c in line:
        if c.isdigit():
            if first == '':
                first = c
            last = c
    print(first+last)
    return int(first+last)

def read_file(file):
    text_file = open("./input/" + file, "r").read().splitlines()
    

    return text_file

part_one('test.txt')
part_one('real.txt')

part_two('test2.txt')
part_two('real.txt')