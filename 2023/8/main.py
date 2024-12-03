from mapNode import MapNode

def testDataOne():
    return """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)"""

def testDataTwo():
    return """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""

def testDataThree():
    return """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""

def parseData(data):
    lines = data.splitlines()
    instructions = lines[0]
    nodes = {}
    for l in lines[2:]:
        n = MapNode(l)
        nodes[n.getId()] = n
    return (instructions,nodes)

def part_one(data):
    (instructions,nodes) = parseData(data)
    startNode = nodes['AAA']
    
    total = 0
    while startNode.getId() != 'ZZZ':
        startNode = MapNode.walkInstructions(instructions,startNode,nodes)
        total += len(instructions)

    return print('P1',str(total))

def part_two(data):
    (instructions,nodes) = parseData(data)
    
    startNodes = list(map(lambda k: nodes[k],filter(lambda n: nodes[n].getGroup() == 'A',nodes)))
    
    total = 0
    # while startNode.getId() != 'ZZZ':

    nodeSteps = []
    for startNode in startNodes:
        steps = 0
        while startNode.getGroup() != 'Z':
            startNode = MapNode.walkInstructions(instructions,startNode,nodes)
            steps += 1
        nodeSteps.append(steps)
    nodeSteps.sort(reverse=True)
    
    # Say we get this from the above
    # [9,7,3]
    # From the first numbers we have to work in steps of 9, from the second steps of 7
    # so 9*7= 63
    # Next we ignore three since 63%3=0
    
    optionCount = 1
    for n in nodeSteps:
        if optionCount == 0 or optionCount%n != 0:
            optionCount *= n
        
    total = len(instructions) * optionCount
    return print('P2',str(total))

def read_file(file):
    return open(file, "r").read()


    
part_one(testDataOne())
part_one(testDataTwo())
part_one(read_file('input.txt'))

part_two(testDataThree())
part_two(read_file('input.txt'))
