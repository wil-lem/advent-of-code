from enum import unique
import re
import statistics

def part_one(file):
    treeMap = read_file(file)
    
    scanBy = [
        [treeMap[0],'bottom'],
        [treeMap[-1],'top'],
        [map(lambda row: row[0],treeMap),'right'],
        [map(lambda row: row[-1],treeMap),'left']
    ]
    
    for info in scanBy:
        trees = info[0]
        for tree in trees:
            prevSize = -1
            while tree:
                if tree.size > prevSize:
                    tree.visible = 1
                    prevSize = tree.size
                tree = getattr(tree,info[1])

    rowCounts = map(lambda row: sum(map(lambda tree: tree.visible,row)),treeMap )
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