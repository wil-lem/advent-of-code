from enum import unique
from fractions import Fraction
import re
import statistics
import sys
import math

def part_one(file):
    data = read_file(file)

    added = addLines(data)
    
    print('P1 ' + file + ': ' + str(added.getMagnitude()))

def part_two(file):
    data = read_file(file)
    highest = False
    magnitude = 0
    for line in data:
        for line2 in data:
            n = addLines([line,line2])
            nMag = n.getMagnitude() 
            if nMag > magnitude:
                # highest = [
                    # nMag, line, line2, n.getLine()
                # ]
                magnitude = nMag


    # print(highest)
    # count = 0

    print('P2 ' + file + ': ' + str(magnitude))

def addLines(lines):
    base = False
    for line in lines:
        n = Pair()
        n.byText(line)
        if not base:
            base = n
        else:
            base = base.add(n)
        base.reduce()
    return base    
    
def read_file(file):
    file_contents = open("./input/" + file, "r").read().splitlines()
    
    return file_contents

def runTests():
    explodeTests = [
        ['[[[[[9,8],1],2],3],4]','[[[[0,9],2],3],4]'],
        ['[7,[6,[5,[4,[3,2]]]]]','[7,[6,[5,[7,0]]]]'],
        ['[[6,[5,[4,[3,2]]]],1]','[[6,[5,[7,0]]],3]'],
        ['[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]','[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]'],
        ['[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]','[[3,[2,[8,0]]],[9,[5,[7,0]]]]'],
    ]

    for expl in explodeTests:
        test1 = Pair()
        test1.byText(expl[0])
        # test1.print()
        test1.explode()
        # test1.print()
        if test1.getLine() == expl[1]:
            print('ok')
        else:
            print('not ok',expl)
            test1.print()

    splitTests = [
        ['[[[[0,7],4],[15,[0,13]]],[1,1]]','[[[[0,7],4],[[7,8],[0,13]]],[1,1]]'],
        ['[[[[0,7],4],[[7,8],[0,13]]],[1,1]]','[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]']
    ]

    for spl in splitTests:
        test1 = Pair()
        test1.byText(spl[0])
        # test1.print()
        test1.split()
        # test1.print()
        if test1.getLine() == spl[1]:
            print('split ok')
        else:
            print('split not ok',spl)
            test1.print()

    completeTests = [
        ['[[[[4,3],4],4],[7,[[8,4],9]]]','[1,1]','[[[[0,7],4],[[7,8],[6,0]]],[8,1]]']
    ]

    for comp in completeTests:
        comp1 = Pair()
        comp2 = Pair()
        comp1.byText(comp[0])
        comp2.byText(comp[1])
        comp3 = comp1.add(comp2)
        comp3.reduce()
        if comp3.getLine() == comp[2]:
            print('comp ok')

    additionTests = [
        [
            [
                '[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]',
                '[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]',
                '[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]',
                '[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]',
                '[7,[5,[[3,8],[1,4]]]]',
                '[[2,[2,2]],[8,[8,1]]]',
                '[2,9]',
                '[1,[[[9,3],9],[[9,0],[0,7]]]]',
                '[[[5,[7,4]],7],1]',
                '[[[[4,2],2],6],[8,7]]',
            ],
            '[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]'
        ]
    ]

    for addi in additionTests:
        base = False
        for i in addi[0]:
            n = Pair()
            n.byText(i)
            if not base:
                base = n
            else:
                base = base.add(n)
            base.reduce()
        if base.getLine() == addi[1]:
            print('addi ok')

    magTest = [
        ['[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]',3488]
    ]
    for mag in magTest:
        n = Pair()
        n.byText(mag[0])
        if n.getMagnitude() == mag[1]:
            print('mag ok')

    completeTest = [
        [
            '[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]',
            '[[[5,[2,8]],4],[5,[[9,9],0]]]',
            '[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]',
            '[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]',
            '[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]',
            '[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]',
            '[[[[5,4],[7,7]],8],[[8,3],8]]',
            '[[9,3],[[9,9],[6,[4,9]]]]',
            '[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]',
            '[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]',
        ],
        '[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]',
        4140
    ]
    base = addLines(completeTest[0])
    if base.getLine() == completeTest[1]:
        print('complete ok')
    if base.getMagnitude() == completeTest[2]:
        print('complete magnitude ok')

class Pair:
    def __init__(self,parent = False):
        self.left = ''
        self.right = ''
        self.leftI = 0
        self.rightI = 0
        self.leftP = False
        self.rightP = False
        self.parent = parent

    def byText(self,line):
        openened = 0
        left = True
        
        for char in line[1:-1]:
            if openened == 0 and char == ',':
                left = False
                continue

            if char == '[':
                openened += 1
                
            if char == ']':
                openened -= 1
            
            if left:
                self.left += char
            else:
                self.right += char
        
        if self.left[0:1] == '[':
            self.leftP = Pair(self)
            self.leftP.byText(self.left)
        else:
            self.leftI = int(self.left)
        
        if self.right[0:1] == '[':
            self.rightP = Pair(self)
            self.rightP.byText(self.right)
        else:
            self.rightI = int(self.right)

    def print(self):
        print('-'*self.getDepth() + self.getLine())
    
    def getLine(self):
        line = '['
        if(self.leftP):
            line += self.leftP.getLine()
        else:
            line += str(self.leftI)
        line += ','
        if(self.rightP):
            line += self.rightP.getLine()
        else:
            line += str(self.rightI)
        
        line += ']'
        return line
    
    def getMagnitude(self):
        s = 0
        if self.leftP:
            s = 3*self.leftP.getMagnitude()
        else:
            s = 3*self.leftI

        if self.rightP:
            s += 2*self.rightP.getMagnitude()
        else:
            s += 2*self.rightI
        return s

    def reduce(self):
        actions = True
        while actions:
            exploded = self.explode()
            if not exploded:
                split = self.split()
            actions = (exploded or split)   

    def add(self,other):
        sum = Pair()
        sum.leftP = self
        sum.rightP = other
        self.parent = sum
        other.parent = sum

        return sum
    
    def isPlainPair(self):
        if not self.rightP and not self.leftP:
            return True
        return False

    def isLeft(self,pair):
        return self.leftP == pair

    def isRight(self,pair):
        return self.rightP == pair

    def getDepth(self):
        if(self.parent):
            return self.parent.getDepth() + 1
        return 0

    # Walk up the tree until we find a pair that this pair is the left part of
    def getPairToRight(self):
        if self.isLeft():
            return

        # if not self.parent:
        #     return False
        # if self.parent.leftP == self:
        #     return self.parent
        # return self.parent.getPairToRight()

    # def getPairToLeft(self,child):
        # if child.isLeft():


        # if not self.parent:
        #     return False
        # if self.parent.rightP == self:
        #     return self.parent
        # return self.parent.getPairToLeft()


    # def getMostLeftPair(self):
    #     if self.leftP:
    #         return
    # 

    

    def getPairWithChildOnLeft(self,child):
        if self.leftP == child:
            return self
        if self.parent:
            return self.parent.getPairWithChildOnLeft(self)
        return False

    def getPairWithChildOnRight(self,child):
        if self.rightP == child:
            return self
        if self.parent:
            return self.parent.getPairWithChildOnRight(self)
        return False

    def addLeft(self,val):
        basePair = self.parent.getPairWithChildOnRight(self)
        if basePair:
            if not basePair.leftP:
                basePair.leftI += val
                return
            
            basePair = basePair.leftP
            while basePair.rightP:
                basePair = basePair.rightP

            basePair.rightI += val
        return

    def addRight(self,val):
        basePair = self.parent.getPairWithChildOnLeft(self)
        if basePair:
            if not basePair.rightP:
                basePair.rightI += val
                return
            
            basePair = basePair.rightP
            while basePair.leftP:
                basePair = basePair.leftP

            basePair.leftI += val
        return

    def explode(self):
        if self.isPlainPair():
            if(self.getDepth() >= 4):
                
                self.addLeft(self.leftI)
                self.addRight(self.rightI)
       
                # Remove yourself
                if self.parent.isLeft(self):  
                    self.parent.leftI = 0
                    self.parent.leftP = False
                else:
                    self.parent.rightI = 0
                    self.parent.rightP = False

                return True
       
        result = False
        if self.leftP:
            result = self.leftP.explode()
        if not result and self.rightP:
            result = self.rightP.explode()
        
        return result
            
    def split(self):
        result = False
        if self.leftP:
            result = self.leftP.split()
        else:
            if self.leftI > 9:
                val = self.leftI/2
                self.leftP = Pair()
                self.leftP.parent = self
                self.leftP.leftI = math.floor(val)
                self.leftP.rightI = math.ceil(val)
                return True
        
        if result:
            return True

        if self.rightP:
            result = self.rightP.split()
        else:    
            if self.rightI > 9:
                val = self.rightI/2
                self.rightP = Pair()
                self.rightP.parent = self
                self.rightP.leftI = math.floor(val)
                self.rightP.rightI = math.ceil(val)
                return True
        
        return result
            
    
part_one('test.txt')
part_one('real.txt')
part_two('test.txt')
part_two('real.txt')
