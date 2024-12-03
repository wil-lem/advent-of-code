
class MapNode:
    def __init__(self,line):
        parts = line.split()
        self.id = parts[0]
        self.left = parts[2][1:-1]
        self.right = parts[3][:-1]
    
    def getId(self):
        return self.id
    
    def getGroup(self):
        return self.id[-1:]

    def getLeft(self):
        return self.left
    
    def getRight(self):
        return self.right
    
    def walkInstructions(instructions,startNode,nodes):
        for i in instructions:
            if i == 'L':
                startNode = nodes[startNode.getLeft()]
            else:
                startNode = nodes[startNode.getRight()]
        return startNode
    
    def walkGhostInstructions(instructions,startNodes,nodes):
        for i in instructions:
            newNodes = []
            for n in startNodes:
                if i == 'L':
                    newNodes.append(nodes[n.getLeft()])
                else:
                    newNodes.append(nodes[n.getRight()])
            startNodes = newNodes
        return startNodes