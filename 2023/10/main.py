from node import Node
from node import Vector
from node import Polygon

def getData(type='t', num=1):
    if type=='t':
        if num==1:
            data = """-L|F7
7S-7|
L|7||
-L-J|
L|-JF"""
        if num==2:
            data = """7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ"""
        if num==3:
            data = """...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
..........."""
    else:
        data=read_file('input.txt')
    return parseData(data)
    
def parseData(data):
    lines = data.splitlines()
    
    return lines

def part_one(type,num):
    lines = getData(type,num)
    total = 0

    points = []
    startNode = False
    for y,line in enumerate(lines):

        if 'S' in line:
            x = line.find('S')
            startNode = Node(Vector(x,y))
            startNode.setChar('S')
            points.append(startNode.v)
    

    connected = startNode.scanAround(lines)
    for v in connected:
        n = Node(v)
        n.setChar(lines[v.y][v.x])
        n.distance = 1
        points.append(n.v)
        startNode.connectNode(n)

    
    # Now we have everything setup, we can start to walk the loop both ways
    startNodes = startNode.connections
    
    complete = False
    while not complete:
        newNodes = []
        
        for n in startNodes:
            nn = n.next()
            nn.setChar(lines[nn.v.y][nn.v.x])
            
            if nn.v in points:
                complete = True
            else:
                n.connectNode(nn)
                points.append(nn.v)
                newNodes.append(nn)
        
        startNodes = newNodes
        
    return print('P1',str(newNodes[0].distance))

def part_two(type,num):
    total = 0
    lines = getData(type,num)
    total = 0
    
    polygon = Polygon()
    points = []
    startNode = False
    for y,line in enumerate(lines):

        if 'S' in line:
            x = line.find('S')
            startNode = Node(Vector(x,y))
            startNode.setChar('S')
            points.append(startNode.v)
            polygon.add(startNode.v)
    
    connected = startNode.scanAround(lines)
    v = connected[0]
    
    n = Node(v)
    n.setChar(lines[v.y][v.x])
    n.distance = 1
    points.append(n.v)
    startNode.connectNode(n)
    if n.isCorner():
        polygon.add(n.v)
            

    # Now we have everything setup, we can start to walk the loop both ways
    startNode = startNode.connections[0]
    
    complete = False
    while not complete:
        nn = startNode.next()
        nn.setChar(lines[nn.v.y][nn.v.x])
        
        if nn.v in points:
            complete = True
        else:
            if nn.isCorner():
                polygon.add(nn.v)
            startNode.connectNode(nn)
            points.append(nn.v)
            
        startNode = nn
        
        
    return print('P2',str(polygon.getArea()))

def read_file(file):
    return open(file, "r").read()



# def connectsTo(c,dir):
#     if dir == 'N':
#         return c in ['|','L','J']
#     if dir == 'S':
#         return c in ['|','F','7']
#     if dir == 'W':
#         return c in ['-','7','J']
#     if dir == 'E':
#         return c in ['-','7','J']

# def getCharVectors(c):
#     dirs = []
#     if c in ['|','L','J']:
#         dirs.append(Vector('y',-1))
#     if c in ['|','F','7']:
#         dirs.append(Vector('y',1))
    
#     if c in ['-','J','7']:
#         dirs.append(Vector('x',-1))
#     if c in ['-','L','F']:
#         dirs.append(Vector('x',1))
    
# # def getConnectingPoints(x,y,map)    

# # class Vector():
# #     def __init__(self,dim,val):
#         self.dim = dim
#         self.val = val

#     # . is ground; there is no pipe in this tile.
#     # S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.


    
part_one('t',1)
part_one('t',2)
# part_one('',0)
part_two('t',3)
# part_two('',0)