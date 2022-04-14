
from enum import unique
import enum
import re
import statistics

def part_one(file):
    map = read_file(file)
    
    # map.print()

    i = 0
    moves = 1
    while moves > 0:
    
        moves = map.step()
        i += 1
        # print(moves,i)
        # map.print()
    
    # count = 0
    print('P1 ' + file + ': ' + str(i))
    
    
def part_two(file):
    map = read_file(file)
    
    count = 0
    print('P2 ' + file + ': ' + str(count))
    

def read_file(file):
    file_contents = open("./input/" + file, "r").read().splitlines()
    
    map = Map()
    for line in file_contents:
        map.addLine(line)

    return map

class Map:
    def __init__(self) -> None:
        self.rows = []
        pass

    def addLine(self,line):
        row = []
        for col in line:
            row.append(col)
        self.rows.append(row)

    def step(self):
        count = 0
        
        # move east
        moves = []
        for r in range(0,len(self.rows)):
            for c in range(0,len(self.rows[0])):
                nextC = c+1
                if nextC > len(self.rows[0])-1:
                    nextC = 0
                
                if self.rows[r][c] == '>' and self.rows[r][nextC] == '.':
                    moves.append([r,c,nextC])
        for move in moves:
            self.rows[move[0]][move[1]] = '.'
            self.rows[move[0]][move[2]] = '>'
        
        count += len(moves)

        # move south
        moves = []
        for r in range(0,len(self.rows)):
            for c in range(0,len(self.rows[0])):
                nextR = r+1
                if nextR > len(self.rows)-1:
                    nextR = 0
                
                if self.rows[r][c] == 'v' and self.rows[nextR][c] == '.':
                    moves.append([r,c,nextR])
        for move in moves:
            self.rows[move[0]][move[1]] = '.'
            self.rows[move[2]][move[1]] = 'v'
        
        count += len(moves)
        return count
              

    def print(self):
        for row in self.rows:
            print(''.join(row))
        print('')


part_one('test.txt')
part_one('real.txt')
# part_two('test.txt')
# part_two('real.txt')
