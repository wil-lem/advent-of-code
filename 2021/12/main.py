from enum import unique
from fractions import Fraction
import re
import statistics

def part_one(file):
    map = read_file(file)
    
    count = 0

    paths = []
    firstPath = Path()
    firstPath.steps.append(map.findOrCreateNode('start'))
    paths.append(firstPath)

    for i in range(100):
        # print('---')    
        oldPaths = paths[:]
        paths = []
        for path in oldPaths:
            if(path.isClosed()):
                paths.append(path)
                continue

            options = path.getOptions()
            for option in options:
                paths.append(path.cloneWithOption(option))
        
        # for path in paths:
        #     path.print()
        
        count = len(list(filter(lambda path: path.isClosed(),paths)))
        if count == len(paths):
            break
    
    print('P1 ' + file + ': ' + str(count))
    
    
def part_two(file):
    map = read_file(file)
    
    count = 0

    paths = []
    firstPath = Path()
    firstPath.steps.append(map.findOrCreateNode('start'))
    paths.append(firstPath)

    for i in range(10000):
        # print('---')    
        oldPaths = paths[:]
        paths = []
        for path in oldPaths:
            if(path.isClosed()):
                paths.append(path)
                continue

            options = path.getOptionsP2()
            for option in options:
                paths.append(path.cloneWithOption(option))
        
        # for path in paths:
            # path.print()
        
        count = len(list(filter(lambda path: path.isClosed(),paths)))
        if count == len(paths):
            break
    
    print('P2 ' + file + ': ' + str(count))


def read_file(file):
    file_contents = open("./input/" + file, "r").read().splitlines()
    rows = []
    map = Map()
    
    for line in file_contents:
        names = re.findall('\w+',line)
        map.addLink(names[0],names[1])
    return map
 
class Map:
    def __init__(self):
        self.nodes = []
    
    def addLink(self,name1,name2):
        node1 = self.findOrCreateNode(name1)
        node2 = self.findOrCreateNode(name2)

        node1.linkNode(node2)

    def findOrCreateNode(self,name):
        for node in self.nodes:
            if node.name == name:
                return node
        
        node = Node(name)
        self.nodes.append(node)
        return node
    
        
    
class Node:
    def __init__(self,name):
        self.name = name
        self.big = self.name == self.name.upper()
        self.start = name == 'start'
        self.end = name == 'end'

        self.links = []

    def linkNode(self,other):
        if other not in self.links:
            self.links.append(other)
        if self not in other.links:
            other.links.append(self)
        
class Path:
    def __init__(self):
        self.steps = []
    
    def getOptions(self):
        options = []
        last = self.steps[-1]
        for next in last.links:
            if next not in self.steps or next.big:
                options.append(next)
        return options
        
    def getOptionsP2(self):
        options = []
        last = self.steps[-1]
        hasDouble = self.hasDoubleSmallCave()
        for next in last.links:
            if next.start:
                continue
            if next.big or next not in self.steps:
                options.append(next)
                continue
            
            #The option is already in the steps, is there already a double small cave in there?
            if hasDouble == False:
                options.append(next)
        
        # print('----')
        # self.print()
        # for step in options:
        #     print('-',step.name)

        return options

    def hasDoubleSmallCave(self):
        steps = []
        double = False
        for step in self.steps:
            if step.start or step.end or step.big:
                continue
            if step in steps:
                double = True
                break
            steps.append(step)
        return double

    def isClosed(self):
        return self.steps[-1].end 

    def cloneWithOption(self,node):
        path = Path()
        path.steps = self.steps[:]
        path.steps.append(node)
        return path
    
    def print(self):
        stepString = ""
        for step in self.steps:
            stepString += step.name + "-"
        print(stepString[0:-1])


    
part_one('test.txt')
part_one('test-larger.txt')
part_one('test-largest.txt')
part_one('real.txt')
part_two('test.txt')
part_two('test-larger.txt')
part_two('test-largest.txt')
part_two('real.txt')
