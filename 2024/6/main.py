import re
from readFile import ReadFile
import time
    
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __str__(self):
        return f'({self.x}, {self.y})'
    
    def clone(self):
        return Vector(self.x, self.y)

    def set(self, axis, value):
        if axis == 'x':
            self.x = value
        else:
            self.y = value
        pass

    def add(self, other):
        self.x += other.x
        self.y += other.y
        pass

    def inGrid(self,w,h):
        return self.x >= 0 and self.x < w and self.y >= 0 and self.y < h
    
class MoveMent:
    def __init__(self, axis, direction):
        self.mod = Vector(0,0)
        self.mod.set(axis, direction)
        pass
    
    def apply(self, point):
        point.add(self.mod)

    def clone(self):
        movement = MoveMent(self.mod.x, self.mod.y)
        movement.mod = self.mod.clone()
        return movement

    def turnClockWise(self):
        if self.mod.x == 0:
            if self.mod.y == 1:
                # Down -> Left
                newMod = Vector(-1, 0)
            else:
                # Up -> Right
                newMod = Vector(1, 0)
        else:
            if self.mod.x == 1:
                # Right -> Down
                newMod = Vector(0, 1)
            else:
                # Left -> Up
                newMod = Vector(0, -1)

        self.mod = newMod

class Map:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.obstructions = {}
        self.guard = None
        self.inSimulation = False

        self.extraObstructions = []
        
        pass

    def addGuard(self, guard):
        self.guard = guard

    def addObstruction(self, x, y):
        self.obstructions[(x,y)] = True
    
    def removeObstruction(self, x, y):
        del self.obstructions[(x, y)]

    def isObstructed(self, x, y):
        return self.obstructions.get((x, y), False)

    def doRoute(self):
        steps = 0
        while self.moveGuard():
            steps += 1
        pass
        
    def moveGuard(self):
        nextPos = self.guard.nextPos()
        if not nextPos.inGrid(self.w, self.h):
            return False
        if self.isObstructed(nextPos.x, nextPos.y):
            self.guard.turn()
            if self.inSimulation and self.guard.inLoop:
                return False
            return True
        else:
            # We can move to the next position, before we move,
            # put an obstruction in the next position and start the simulation
            if not self.inSimulation:
                self.simulateObstacle(nextPos)
                

            self.guard.moveToNext(nextPos)
            
            if self.inSimulation and self.guard.inLoop:
                return False
            return True
        
    def simulateObstacle(self,nextPos):
        self.inSimulation = True
        self.guard.saveState()
        self.addObstruction(nextPos.x, nextPos.y)

        self.doRoute()
        if self.guard.inLoop and nextPos not in self.extraObstructions:
            self.extraObstructions.append(nextPos.clone())
        
        self.removeObstruction(nextPos.x, nextPos.y)
        self.guard.restoreState()
        self.inSimulation = False

        # Add extra obstruction
        # self.detectLoop = True

        # self.detectLoop = False

    def printMap(self):
        for y in range(self.h):
            for x in range(self.w):
                if self.isObstructed(x, y):
                    print('#', end='')
                elif Vector(x, y) in self.extraObstructions:
                    print('O', end='')
                elif self.guard.pointsOnRoute.get((x, y), False):
                    print('X', end='')
                else:
                    print('.', end='')
            print()
        pass

        
class Guard:
    def __init__(self, x, y, axis, direction):
        self.position = Vector(x, y)
        self.movement = MoveMent(axis, direction)
        self.pointsOnRoute = {}
        self.states = {}
        self.inLoop = False
        pass

    def nextPos(self):
        pos = self.position.clone()
        self.movement.apply(pos)
        return pos
    
    def turn(self):
        self.movement.turnClockWise()

        key = self.getStateKey()
        if self.hasState(key):
            self.inLoop = True
            return
        self.addState(key)


    def addPointOnRoute(self, point):
        self.pointsOnRoute[(point.x, point.y)] = True

    def addState(self, state):
        self.states[state] = True

    def hasState(self, state):
        return self.states.get(state, False)

    def getStateKey(self):
        return f"{self.position.x},{self.position.y},{self.movement.mod.x},{self.movement.mod.y}"

    def moveToNext(self, nextPos):
        # nextPos = self.nextPos()
        self.addPointOnRoute(nextPos)
        self.position = nextPos

        key = self.getStateKey()
        if self.hasState(key):
            self.inLoop = True
            return
        self.addState(key)


    def saveState(self):
        self.savedStates = self.states.copy()
        self.savedPosition = self.position.clone()
        self.savedMovement = self.movement.clone()
        self.savedPointsOnRoute = self.pointsOnRoute.copy()
    
    def restoreState(self):
        self.states = self.savedStates
        self.position = self.savedPosition
        self.movement = self.savedMovement
        self.pointsOnRoute = self.savedPointsOnRoute
        self.inLoop = False


def one(fileName):
    # Track the time it takes to solve the problem
    start = time.time()

    rf = ReadFile('input/' + fileName + '.txt')
    lines = rf.getLines()
    w = h = 0
    h = len(lines)
    w = len(lines[0].strip())
    startPos = Vector(0, 0)

    map = Map(w, h)
    
    for y in range(h):
        for x in range(w):
            char = lines[y][x]
            if char == '#':
                map.addObstruction(x, y)
            elif char == '^':
                guard = Guard(x, y, 'y', -1)
                map.addGuard(guard)
                startPos = Vector(x, y)

    map.doRoute()
    print('Points visited:', len(map.guard.pointsOnRoute))
    print('Extra obstructions:', len(map.extraObstructions))
    print('Start poistion in obstruction:', startPos in map.extraObstructions)
    
    outsideGrid = [obs for obs in map.extraObstructions if not obs.inGrid(w, h)]
    doubeObstructions = [obs for obs in map.extraObstructions if map.isObstructed(obs.x, obs.y)]
    print('Outside grid:', len(outsideGrid))
    print('Bouble obs:', len(doubeObstructions))
    

    # map.printMap()
    end = time.time()
    print(f"Time: {end - start}")

one('test')
one('real')

