from enum import unique
from fractions import Fraction
import re
import statistics

def part_one(file):
    data = read_file(file)
    score = 0 
    for i in data:
        hisMove = translateMove(i[0:1])-1
        myMove = translateMove(i[-1:])
        score += myMove + 3* ((myMove-hisMove) % 3)    
    print(score)
        
def part_two(file):
    data = read_file(file)
    score = 0 
    for i in data:
        hisMove = translateMove(i[0:1])
        gameOutCome = translateMove(i[-1:])-2
        score += (hisMove + gameOutCome -1) % 3 + 4 + 3*gameOutCome    
    print(score)

def read_file(file):
    return open("./input/" + file, "r").read().splitlines()
    

def translateMove(input):
    if input == 'A' or input == 'X':
        return 1
    if input == 'B' or input == 'Y':
        return 2
    return 3
    


part_one('test.txt')
part_one('real.txt')
part_two('test.txt')
part_two('real.txt')
