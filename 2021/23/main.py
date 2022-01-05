from enum import unique
from fractions import Fraction
from os import stat
import math
import re
import statistics

def part_one(file):
   
    map = read_file(file)
    map.setAllowedMoves()    

    # map.move({"origin":map.nodes[13],"node":map.nodes[7],"size":4})
    # n = map.nodes[12]
    # m = map.getMoves(n)
    # print(m)
    map.print()

    # for node in map.nodes:
        # print(map.nodes.index(node),node.title(),node.open,node.shouldMove) 
    map.step()

    answer = map.spentEnergy
    print('P1 ' + file + ': ' + str(answer))
    
    
def part_two(file):
    map = read_file(file)
    map.print()
    map.setAllowedMoves()

    # n = map.nodes[13]
    map.step()
    
    # moves = map.getPossibleMoves()
    # print(moves)
    answer = 0
    print('P2 ' + file + ': ' + str(answer))


def read_file(file):
    file_contents = open("./input/" + file, "r").read().splitlines()
    
    map = Map()
    
    for line in file_contents[2:]:
        letters = re.findall('[A-Z]',line)
        if letters:
            for letter in letters:
                n = Node(len(map.nodes))
                o = Amphipod(letter)
                n.setOccupant(o)
                n.type = 'room'
                map.nodes.append(n)
                
                col = (n.ind - 11)%4
                if col == 0:
                    n.accept = 'A'
                if col == 1:
                    n.accept = 'B'
                if col == 2:
                    n.accept = 'C'
                if col == 3:
                    n.accept = 'D'

                if n.ind < 15:
                    map.connectNodes(n.ind,n.ind*2-20)
                else:
                    map.connectNodes(n.ind,n.ind-4)
                    


    # letters = re.findall('[A-Z]',file_contents[2]) + re.findall('[A-Z]',file_contents[3]) 
    # if letters:

    # i = 11
    # for letter in letters:
        
    #     map.nodes[i].setOccupant(Amphipod(letter))
    #     i += 1
    
    return map

class Map():
    def __init__(self):
        self.nodes = []
        self.spentEnergy = 0
        self.bestSolution = False
        self.steps = []
        self.states = []

        for i in range(0,11):
            node = Node(i)
            self.nodes.append(node)
            # if i > 10:
                # node.type = 'room'

        for i in range(1,11):
            self.nodes[i].connect(self.nodes[i-1])

        self.nodes[2].type = 'exit'
        self.nodes[4].type = 'exit'
        self.nodes[6].type = 'exit'
        self.nodes[8].type = 'exit'

        

    def allDone(self):
        for n in self.nodes:
            if n.isHallway():
                continue
            if not n.occupant:
                return False
            if n.occupant.type != n.accept:
                return False
        return True

    def move(self,path):
        origin = path['origin']
        target = path['node']

        target.setOccupant(origin.occupant)
        origin.setOccupant(False)
        
        self.spentEnergy += path['size'] * target.occupant.getEnergy()
        self.steps.append('Moved ' + str(target.occupant) + ' ' + origin.title() + '=>' + target.title()) 

    def undoMove(self,path):
        origin = path['origin']
        target = path['node']
        
        origin.setOccupant(target.occupant)
        target.setOccupant(False)

        self.spentEnergy -= path['size'] * origin.occupant.getEnergy()
        self.steps = self.steps[0:-1]
    

    def connectNodes(self,i,j):
        self.nodes[i].connect(self.nodes[j])


    def print(self):
        print('#'*13)
        line = '#'
        for i,node in enumerate(self.nodes):
            line += str(node)
            if i > 10:
                line += '#'
            if i == 10:
                line += '#'
                print(line)
                line = '#'*3
            if i == 14:
                line += '##'
                print(line)
                line = '  #'
            if i == 18 or i == 22:
                print(line)
                line = '  #'
            
        print(line)
        print('  ' + '#'*9)
        print('Energy spent',self.spentEnergy)
        for i in self.steps:
            print(i)
        print()
    
    def getPossibleMoves(self):
        moveableNodes = self.getNodesWithMoveableOccupant()
    
        moves = []
        for n in moveableNodes:
            moves += self.getMoves(n)
        return moves

    def getMoves(self,node):
        paths = []
        node.getPaths(paths,node,0,False)
        
        # If we're in a hallway we're only allowed to move into a room
        if node.isHallway():
            # print('H')
            roomPaths = []
            for path in paths:
                # print('->',path['node'].title())
                # if path['node'].isHallway():
                #     continue
                # # print(2)
                # if not path['node'].acceptAmphipod(node.occupant):
                #     continue
                # print(3)
                
                if not path['node'].isBottom():
                    # bottomNode = next((x for x in path['node'].connections if x.isBottom()),False)
                    below = path['node'].getBelow()
                    bottomNode = below[0]
                    if bottomNode.isEmpty():
                        # We don't want to move to the top part of a room if the bottom is empty
                        continue
                    if bottomNode.shouldMove:
                        # The bottom node is occupied with a different type of amiphod, do not move here
                        continue
                
                # If we reach this point just add the node
                roomPaths.append(path)
            return roomPaths
        else:
            hallPaths = []
            
           
            # Some paths don't allow stops
            for path in paths:
                if path['node'].isHallway():
                    hallPaths.append(path)
                else:
                    # We don't want to move within a chamber
                    if path['node'].accept == path['origin'].accept:
                        continue
                    # print('-->',path['node'].title())
                
                    # If we can move the node directly into another room, we directly want to do that
                    # and not offer any other options
                    if not path['node'].acceptAmphipod(node.occupant):
                        continue
                    
                    below = path['node'].getBelow()
                    if below:
                        bottomNode = below[0]

                        if bottomNode.isEmpty():
                            # We don't want to move to the top part of a room if the bottom is empty
                            continue
                        if bottomNode.shouldMove:
                            # The bottom node is occupied with a different type of amiphod, do not move here
                            continue
                    return [path]
                    

            return hallPaths
            
        
        return paths

    def getNodesWithMoveableOccupant(self):
        nodes = []
        for node in self.nodes:
            if node.occupantShouldMove():
                nodes.append(node)
        return nodes

    

    def step(self):
        if len(self.steps) == 40:
            self.print()
            
        if len(self.steps) < 6:
            state = self.getStateString()
            if state in self.states:
                return
            self.states.append(state)
        # print(state)

        if self.allDone():
            # self.print()
        
            if not self.bestSolution or self.bestSolution['score'] > self.spentEnergy:
                self.bestSolution = {
                    'score': self.spentEnergy,
                    'steps': self.steps[:]
                }
                self.print()
            return
        
        
        if self.bestSolution and self.spentEnergy >= self.bestSolution['score']:
            return
        
        moves = self.getPossibleMoves()
        if len(moves):
            for m in moves:
                self.move(m)
                self.step()
                self.undoMove(m)
        
        
            
            
        # else:
            # print('no more moves')
            # self.print()
            # print(self.nodes[5].title(),self.nodes[5].occupant,self.nodes[5].shouldMove)
            # if self.nodes[5].shouldMove:
            #     moves = self.getMoves(self.nodes[5])
            #     print(moves)
            
            # print(self.nodes[13].title(),self.nodes[13].open)

    def getStateString(self):
        data = str(len(self.steps))
        for n in self.nodes:
            data += str(n)
        
        return data

    def setAllowedMoves(self):
        nodes = self.nodes[:]
        nodes.sort(reverse=True,key=lambda n: n.ind)

        for n in nodes:
            if not n.occupant:
                n.open = True
                n.shouldMove = False
                continue
            
            n.open = False

            correct = n.hasCorrectOccupant()
            
            below = n.getBelow()
            if below:
                if below[0].shouldMove or below[0].open:
                    n.shouldMove = True
                    continue
            n.shouldMove = (not correct)
        
        for n in self.nodes:
            print(n.shouldMove,n.title())

class Node:
    def __init__(self,i):
        self.connections = []
        self.type = 'hallway'
        self.occupant = False
        self.accept = False
        self.ind = i
        self.shouldMove = False
        self.open = True

        self.top = False
        self.bottom = False
        
    def __str__(self):
        if self.occupant:
            return str(self.occupant)
        return '.'

    def title(self):
        if self.type == 'hallway':
            return 'H' + str(self.ind)
        
        if self.type == 'exit':
            return 'Exit: ' + str(self.ind)
        
        if not self.isHallway():
            return 'Room ' + self.accept + '-' + str(self.getDepth())
            
        return str(self.ind)
    
    def getDepth(self):
        return math.floor((self.ind - 11)/4)

    def connect(self,other):
        self.connections.append(other)
        other.connections.append(self)
        
    def setTop(self,other):
        self.top = other
        other.bottom = self

    def isHallway(self):
        return (self.type == 'hallway' or self.type =='exit')

    def allowStop(self):
        if self.type =='exit':
            return False
        if self.isHallway():
            return True
        below = self.getBelow()
        if not below:
            return True
        if below[0].isEmpty():
            return False
        return True

    def isBottom(self):
        if self.isHallway():
            return False
        return len(self.connections) == 1

    def isEmpty(self):
        return self.occupant == False

    def acceptAmphipod(self,amphipod):
        return self.accept == amphipod.type

    def hasCorrectOccupant(self):
        if self.isEmpty():
            return False
        return self.acceptAmphipod(self.occupant)


    def occupantShouldMove(self):
        return self.shouldMove

        if not self.occupant:
            return False
        if self.isHallway():
            return True
        if not self.acceptAmphipod(self.occupant):
            return True
        
        #occupant is in the correct room
        # If this is the bottom part of the room the occupant can stay
        if self.isBottom():
            return False
        
        # If the bottom is empty or contains the wrong type of amphipod, a move is still neccessary
        bottomNode = next((x for x in self.connections if x.isBottom()),False)
        if not bottomNode.occupant:
            return True
        if not bottomNode.acceptAmphipod(bottomNode.occupant):
            return True
        return False

    def getPaths(self,paths,originNode,size,prevNode):
        for n in self.connections:
            if n == prevNode:
                continue
            if not n.open:
                continue
            if self.type == 'exit' and n.type == 'room' and n.accept and n.accept != originNode.occupant.type:
                continue

            n.getPaths(paths,originNode,size+1,self)
        
        if self == originNode or (originNode.isHallway() and self.isHallway()) or not self.allowStop():
           return 
        
        paths.append({'node':self, 'size':size, 'origin': originNode})
        
        
    def setOccupant(self,occupant):
        self.occupant = occupant
        if not self.occupant:
            self.shouldMove = False
            self.open = True
            return


        # There is an occupant
        self.open = False
        if self.isHallway():
            self.shouldMove = True
            return

        below = self.getBelow()
        if(below):
            if below[0].shouldMove:
                self.shouldMove = True
                return
        
        # Nothing below
        if self.acceptAmphipod(self.occupant):
            self.shouldMove = False
            return
        
        self.shouldMove = True

    def getBelow(self):
        below = []
        for n in self.connections:
            if n.ind < self.ind:
                continue
            below.append(n)
            below += n.getBelow()
        return below

    def getAbove(self):
        above = []
        for n in self.connections:
            if n.ind > self.ind:
                continue
            if n.isHallway():
                continue
            above.append(n)
            above += n.getAbove()
        return above

class Amphipod:
    def __init__(self,type) -> None:
        self.type = type
    def __str__(self) -> str:
        return self.type

    def getEnergy(self):
        if self.type == 'A':
            return 1
        if self.type == 'B':
            return 10
        if self.type == 'C':
            return 100
        if self.type == 'D':
            return 1000
        return False

# part_one('test.txt')
# part_one('real.txt')
# part_two('test2.txt')
part_two('real2.txt')
