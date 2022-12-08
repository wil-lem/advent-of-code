from enum import unique
import re
import statistics

def part_one(file):
    treeMap = read_file(file)
    
    # Look from left
    for row in treeMap:
        prevSize = -1
        for tree in row:
            if tree.size > prevSize:
                tree.visible += 1
                prevSize = tree.size
        
    # Look from right
    prevSize = -1
    for tree in row[::-1]:
        if tree.size > prevSize:
            tree.visible += 1
            prevSize = tree.size

    # Look from top to bottom
    for col in range(0,len(treeMap[0])):
        prevSize = -1
        for row in treeMap:
            tree = row[col]
            
            if tree.size > prevSize:
                tree.visible += 1
                prevSize = tree.size

    # Look from bottom to top
    prevSize = -1
    for row in treeMap[::-1]:
        tree = row[col]
        if tree.size > prevSize:
            tree.visible += 1
            prevSize = tree.size
    
    
    rowCounts = map(lambda row: sum(map(lambda tree: 1 if tree.visible > 0 else 0,row)),treeMap )
    print(sum(rowCounts))
    
    
def part_two(file):
    grid = read_file(file)
    
    score = 0
    for row in grid[1:-1]:
        for tree in row[1:-1]:
            score = max(tree.getViewScore(),score)
    print(score)
    
def read_file(file):
    grid = open("./input/" + file, "r").read().splitlines()

    treeMap = []

    for y,line in enumerate(grid):
        row = []
        for x,size in enumerate(line):
            row.append(Tree(int(size)))
            if x > 0:
                row[x].connectLeft(row[x-1])
            if y > 0:
                row[x].connectTop(treeMap[y-1][x])
                
        treeMap.append(row)
    return treeMap


class Tree:
    def __init__(self,size) -> None:
        self.size = size
        self.visible = 0
        self.top = False
        self.bottom = False
        self.right = False
        self.left = False
        
        pass
    
    def connectLeft(self,other):
        self.left = other
        other.right = self
    
    def connectTop(self,other):
        self.top = other
        other.bottom = self
    
    def getDirectionViewScore(self,direction):
        nextTree = getattr(self,direction)
        score = 0
        while nextTree:
            score += 1
            if nextTree.size >= self.size:
                break
            
            nextTree = getattr(nextTree,direction)
        return score

    def getViewScore(self):
        scores = 1
        for dir in ['top','right','bottom','left']:
            scores *= self.getDirectionViewScore(dir)
        return scores
    
part_one('test.txt')
part_one('real.txt')
part_two('test.txt')
part_two('real.txt')