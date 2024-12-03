import re
import math
from typing import ChainMap


def part_one(file):
    games = read_file(file)
    testDraw = Draw()
    testDraw.fromRGB(12,13,14)
    total = 0
    for game in games:
        if game.fitsInto(testDraw):
            total += int(game.id)

    return print('P1 - ' + file + ': ' + str(total))

def part_two(file):
    games = read_file(file)
    total = 0
    for game in games:
        total += game.getPower()
    return print('P2 - ' + file + ': ' + str(total))

class Game:
    def __init__(self,line) -> None:
        self.draws = []
        
        parts = line.split(':')
        self.id = int(parts[0][4:])
        draws = parts[1].split(';')
        for draw in draws:
            oDraw = Draw()
            oDraw.fromText(draw)
            self.draws.append(oDraw)

    def fitsInto(self,testDraw):
        for draw in self.draws:
            if not draw.fitsInto(testDraw):
               return False
        return True
    
    def getPower(self):
        powerDraw = Draw()
        for draw in self.draws:
            powerDraw.addDraw(draw)
        return powerDraw.getPower()
    
class Draw:
    def __init__(self) -> None:
        self.red = 0
        self.green = 0
        self.blue = 0
    
    def fromText(self,line):
        m = re.findall(r"([0-9]+) ([a-z]+)",line)
        for i in m:
            setattr(self,i[1],int(i[0]))
    
    def fromRGB(self,r,g,b):
        self.red = r
        self.green = g
        self.blue = b

    def fitsInto(self,other):
        return (self.red <= other.red and self.green <= other.green and self.blue <= other.blue)
    
    def addDraw(self,other):
        self.red = max(other.red,self.red)
        self.green = max(other.green,self.green)
        self.blue = max(other.blue,self.blue)
    
    def getPower(self):
        return self.red * self.green * self.blue

def read_file(file):
    text_file = open("./input/" + file, "r").read().splitlines()
    games = []
    for line in text_file:
        games.append(Game(line))

    return games

part_one('test.txt')
part_one('real.txt')

part_two('test.txt')
part_two('real.txt')