from enum import unique
from fractions import Fraction
import re
import statistics

def part_one(file):
    map = read_file(file)
    
    count = 0
    for i in range(1,101):
        count += map.step()
        
    print('P1 ' + file + ': ' + str(count))
    
    
def part_two(file):
    map = read_file(file)
    size = len(map.rows[0])*len(map.rows)

    f = 0
    i = 0
    while f < 1:
        f = map.step() / size
        i += 1
        
    print('P2 ' + file + ': ' + str(i))


def read_file(file):
    file_contents = open("./input/" + file, "r").read().splitlines()
    rows = []
    map = Map()
    
    for row,cols in enumerate(file_contents):
        for col,number in enumerate(cols):
            map.addPoint(Point(col,row,int(number)))
    map.linkPoints()
    return map
 
class Map:
    def __init__(self):
        self.rows = []
    
    def addPoint(self, point):
        while point.x >= len(self.rows):
            self.rows.append([])
        while point.y >= len(self.rows[point.x]):
            self.rows[point.x].append([])
        self.rows[point.x][point.y] = point

    
    def linkPoints(self):
        for x,row in enumerate(self.rows):
            for y,point in enumerate(row):
                self.linkPoint(point)

    def linkPoint(self,point):
        if self.getPoint(point.x-1,point.y):
            point.linkW(self.getPoint(point.x-1,point.y))

        if self.getPoint(point.x-1,point.y-1):
            point.linkNW(self.getPoint(point.x-1,point.y-1))
        
        if self.getPoint(point.x,point.y-1):
            point.linkN(self.getPoint(point.x,point.y-1))
        
        if self.getPoint(point.x+1,point.y-1):
            point.linkNE(self.getPoint(point.x+1,point.y-1))

    def getPoint(self,x,y):
        if x >= 0 and x < len(self.rows) :
            if y >= 0 and y < len(self.rows[y]) :
                return self.rows[x][y]
        return False
        
    def printMap(self):
        printRows = ['']*10
        for x,row in enumerate(self.rows):
            rowString = ""
            for y,point in enumerate(row):
                printRows[y] += str(point.val)

        for printRow in printRows:
            print(printRow)
        

    def step(self):
        

        flashes = 0
        for row in self.rows:
            for point in row:
                point.val += 1
        
        for row in self.rows:
            for point in row:
                point.step()
        

        # Reset flashed and count
        for row in self.rows:
            for point in row:
                if point.flashed:
                    flashes += 1
                    point.flashed = False
                    point.val = 0
        
        return flashes
    
    def debugPoint(self,x,y):
        point = self.rows[x][y]
        
        line = '' 
        line += str(point.dnw.val) if point.dnw else '-'
        line += str(point.dn.val) if point.dn else '-'
        line += str(point.dne.val) if point.dne else '-'
        print(line)

        line = '' 
        line += str(point.dw.val) if point.dw else '-'
        line += str(point.val)
        line += str(point.de.val) if point.de else '-'
        print(line)
        
        line = '' 
        line += str(point.dsw.val) if point.dsw else '-'
        line += str(point.ds.val) if point.ds else '-'
        line += str(point.dse.val) if point.dse else '-'
        print(line)

        
        
    
class Point:
    def __init__(self,x,y,val):
        self.x = x
        self.y = y
        self.val = int(val)

        self.dn = False
        self.dne = False
        self.de = False
        self.dse = False
        self.ds = False
        self.dsw = False
        self.dw = False
        self.dnw = False

        self.flashed = False
    
    def linkW(self,other):
        self.dw = other
        other.de = self
    
    def linkN(self,other):
        self.dn = other
        other.ds = self
    
    def linkNW(self,other):
        self.dnw = other
        other.dse = self

    def linkNE(self,other):
        self.dne = other
        other.dsw = self
    
    def step(self):
        if self.val > 9:
            self.flash()
    
    def flash(self):
        if self.flashed:
            return
        if self.val > 9:
            self.flashed = True
            # print('f-',self.x,self.y)
            if self.dnw: 
                self.dnw.adjacentFlashed()
            if self.dn: 
                self.dn.adjacentFlashed()
            if self.dne: 
                self.dne.adjacentFlashed()
            
            if self.dw: 
                self.dw.adjacentFlashed() 
            if self.de: 
                self.de.adjacentFlashed()
            
            if self.dse: 
                self.dse.adjacentFlashed()
            if self.ds: 
                self.ds.adjacentFlashed() 
            if self.dsw: 
                self.dsw.adjacentFlashed()
            
            # print('-f',self.x,self.y)
    def adjacentFlashed(self):
        # print('a flash',self.x,self.y)
        # if self.flashed:
        #     return
        self.val += 1
        if self.val > 9:
            self.flash()


    
part_one('test.txt')
part_one('real.txt')
part_two('test.txt')
part_two('real.txt')
