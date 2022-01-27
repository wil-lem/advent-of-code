from enum import unique
from os import stat
import re
import statistics
import math

def part_one_test(file):
    lines = read_file(file)
    
    # alu = ALU(lines)
    
    # for i in range(0,10):
    #     alu.run(str(i))
    #     print(i,'--',alu)
    

def parseRange(lines,eqmod):
    inputRange = []

    # Get variable elements
    for i,line in enumerate(lines):
        if i%18 == eqmod:
            inputRange.append(int(re.match('.*?([\-0-9]+)',line)[1]))
    return inputRange



def findMaxNumber(lines):

    divisions = parseRange(lines,4)
    additionsX = parseRange(lines,5)
    additionsY = parseRange(lines,15)

    print('d',divisions)
    print('x',additionsX)
    print('y',additionsY)

    w = 0
    x = 0
    y = 0
    z = 0

    dL = [1,  1,  1,  1,  1,  26,  1,   26,  26,  1,   26,   26,   26,  26]
    xL = [13, 11, 12, 10, 14, -1,  14,  -16, -8,  12,  -16,  -13,  -6,  -6]
    yL = [6,  11, 5,  6,  8,  14,  9,   4,   7,   13,  11,   11,   6,   1]
    # 14991881741191
    # y values: 7 15 14 15 9 0 17 0 0 17 0 0 0 0
    # x values: 
    inputString = '13579246899999'
    inputString = '99999'
    
    
    
    while len(inputString) < 14:
        a = 9
        minZ = False
        bestA = False
        
        while a > 0:
            testInputString = str(a) + inputString
            z = programRun(testInputString,lines)
            if not bestA or z < minZ:
                minZ = z
                bestA = str(a)
            a -= 1
        inputString = bestA + inputString

        print('i,z',inputString,programRun(inputString,lines))
    # test = '99'
    # print(programRun(test,lines))

    # for pos in range(0,14):
        # print('pos',pos)
        # a = 9
        # while a > 0:
        #     zt = program(a, z, additionsX[pos], divisions[pos], additionsY[pos])
        #     print('a',pos,a,zt)
            # a -= 1
        # z = zt
        

def part_one(file):
    print('========')
    lines = read_file(file)
    alu = ALU(lines)
    
    # base = 11991881741191
    
    # z = 9999999999999999999
    # for i in range(0,1000):
    #     strBase = str(base)
    #     if '0' not in strBase:

    #         alu.run(strBase)
    #         if alu.mem['z'] <= z:
    #             print('smaller',strBase)
    #             print('test   ',alu)
    #             z = alu.mem['z']
    #     base += 1000000000000
    #     if base > 99999999999999:
    #         break 

    inputString = '13579246899999'
    inputString = '15000000000000'
    inputString = '14991881741191'
    


   
    # Get the list items for the variable parts of the repeating program 
    dL = parseRange(lines,4)
    xL = parseRange(lines,5)
    yL = parseRange(lines,15)

    inputString = findMaxNumberByPairs(dL,xL,yL)
    alu.run(inputString)
    # programRun(inputString,lines,dL,xL,yL,26)

    # # The program stores the letters in multiples of 26 
    # # Let's run a very simple program
    # dL = [1,1,1000,1000] # This is vital, the program will multiply by 26 at some point, so we need the other 26 to balance this
    # xL = [1,3,-5,-4] # This is added to the z%26 so we have to make it negative if we want to make it match the input
    # yL = [7,4,9,4]
    # programRun('2215',lines,dL,xL,yL,1000)


    
    print('P1 ' + file + ': ' + findMaxNumberByPairs(dL,xL,yL))
    

def part_two(file):

    lines = read_file(file)
    
    alu = ALU(lines)
    
    # Get the list items for the variable parts of the repeating program 
    dL = parseRange(lines,4)
    xL = parseRange(lines,5)
    yL = parseRange(lines,15)


    alu.run(findMinNumberByPairs(dL,xL,yL))
    print('P2 ' + file + ': ' + findMinNumberByPairs(dL,xL,yL))


# The program is just a 14x repetition of this code, all that's variable in the instructions is d,aX and aY
# these are the variable parts:
# 
# d [1,  1,  1,  1,  1,  26, 1,  26,  26, 1,  26,  26,  26, 26] (always 1 or 26)
# x [13, 11, 12, 10, 14, -1, 14, -16, -8, 12, -16, -13, -6, -6] (always smaller than 0 or bigger than 10)
# y [6,  11, 5,  6,  8,  14, 9,  4,   7,  13, 11,  11,  6,  1] (always positive and <= 13)
#
# This program may be easier to understand if we replace 26 by 1000
# Each step has it's own instructions. Say we arrive at some step with
# inputVal = 5
# z = 145.135.122
# d = 1 
# aX = 30
# aY = 44  
# 
# x = z%1000 + aX           x = 122 + 30 = 152  
# z = math.floor(z/d)       z = 145.135.122
# x != inputVal
# z *= 1000                 z = 145.135.122.000
# z += inputVal + aY        z = 145.135.122.000 + 5 + 44 = 145.135.122.049
# 
# So basically what we did is save the input value in the last part of z with a modifier
# 
# ------
# Now let's do it the other way round
# z = 145.135.122
# inputVal = 5
# d = 1000 
# aX = -30
# aY = 44  
#  
# x = z%1000 + aX           x = 122 - 30 = 92  
# z = math.floor(z/d)       z = 145.135
# x != inputVal
# z *= 1000                 z = 145.135.000
# z += inputVal + aY        z = 145.135.000 + 5 + 44 = 145.135.049
#
# So within z we've replaced the last part with the new input + the modifier
#
# Version number:
# To get back to zero, we will first (at i) add a number to z (inputi+aYi), at the end (Ri), we will get this number back but x will be added to it (inputi+aYi+ayRi)
# so inputRi = inputi + aYi + ayRi
# 
# So for the above d,x,y lists, if the first input i '1' the last input will have to be 1+6-6=1
# Second input '4' -> 4+11-6 = 9
# There are some more constraints used in the following function

def findMaxNumberByPairs(dL,xL,yL):
    vals = []
    firstNumberIndexes = []
    for i in range(0,14):
        d = dL[i]
        if(d == 1):
            # Save the number for now
            vals.append(9)
            firstNumberIndexes.append(i)
        else:
            pairI = firstNumberIndexes[-1]
            x = xL[i]
            y = yL[pairI]
            
            # Go for the max
            sVal = 9
            tVal = sVal+x+y
            
            # Reduce if needed
            if tVal > 9:
                diff = tVal - 9
                sVal -= diff
                tVal -= diff


            vals.append(tVal)
            vals[pairI] = sVal
            firstNumberIndexes = firstNumberIndexes[0:-1]
            
    code = ''
    for v in vals:
        code += str(v)
    return code


def findMinNumberByPairs(dL,xL,yL):
    vals = []
    firstNumberIndexes = []
    for i in range(0,14):
        d = dL[i]
        if(d == 1):
            # Save the number for now
            vals.append(9)
            firstNumberIndexes.append(i)
        else:
            pairI = firstNumberIndexes[-1]
            x = xL[i]
            y = yL[pairI]
            
            # Go for the max
            sVal = 1
            tVal = sVal+x+y
            
            # # Reduce if needed
            if tVal < 1:
                diff = 1 - tVal
                sVal += diff
                tVal += diff

            vals.append(tVal)
            vals[pairI] = sVal
            firstNumberIndexes = firstNumberIndexes[0:-1]
            
    code = ''
    for v in vals:
        code += str(v)
    return code



    
def program(inputVal,z,aX,d,aY,modifier):
    print('s',inputVal,z)

    # x = aX, if z contains a remainder add that too
    # 
    x = z%modifier + aX

    # Divide z by modifier if neccessary
    z = math.floor(z/d)

    print('x,w,z',x,inputVal,z)
    
    # The only times x==w is when 
    if x != inputVal:
        # Move z up one "level" and save the input
        z *= modifier
        z += inputVal + aY
    print('=>',z)
    return z

    # Say we have a very simple input array


    # Any time d is 1 we can plug in a value that will be used 
    
    
def programRun(versionNumber,lines,divisions,additionsX,additionsY,modifier):
    w = 0
    x = 0
    y = 0
    z = 0
    
    # divisions = parseRange(lines,4)[-1*len(versionNumber):]
    # additionsX = parseRange(lines,5)[-1*len(versionNumber):]
    # additionsY = parseRange(lines,15)[-1*len(versionNumber):]
    
    z = 0 
    

    # This is the actual program that's repeated every time
    for i in range(0,len(versionNumber)):
        z = program(int(versionNumber[i:i+1]), z, additionsX[i], divisions[i], additionsY[i],modifier)
        # w = data[0]
        # x = data[1]
        # z = data[2]
        
    
    print('program',str(w),str(x),str(y),str(z))

    return z




def read_file(file):
    lines = open("./input/" + file, "r").read().splitlines()
    
    return lines


class ALU:
    def __init__(self,lines) -> None:
        self.mem = {
            'w': 0,
            'x': 0,
            'y': 0,
            'z': 0,
        }
        self.lines = lines
        self.inputInd = 0
        self.inputString = False
    
    def __str__(self) -> str:
        return 'w:' + str(self.mem['w']) + '  x:' + str(self.mem['x']) + '  y:' + str(self.mem['y']) + '  z:' + str(self.mem['z'])

    def reset(self):
        self.mem = {
            'w': 0,
            'x': 0,
            'y': 0,
            'z': 0,
        }
        self.inputInd = 0
        
    def run(self, inputString):
        self.reset()
        self.inputString = inputString
    
        for line in self.lines:
            self.runInstruction(line)
            # print(line,self)
        
    def runInstruction(self, intstruction):
        command = re.match('^([a-z]+) ([wxyz])',intstruction)
        action = command[1]
        address = command[2]

        if action == 'inp':
            self.runInput(address)
            return

        secondArg = re.match('^.*?([\-0-9]+)',intstruction)
        
        secondArgVal = False
        
        if secondArg:
            secondArgVal = int(secondArg[1])
        
        else:
            secondArg = re.match('^.*?([wxyz])$',intstruction)
            secondArgVal = int(self.mem[secondArg[1]])
            
        if action == 'add':
            self.mem[address] += secondArgVal
            return
        
        if action == 'mul':
            self.mem[address] *= secondArgVal
            return

        if action == 'div':
            if secondArgVal == 0:
                raise Exception('Division by zero')
            
            div = self.mem[address] / secondArgVal
            # print('div',self.mem[addresss],secondArgVal,div,math.floor(div))
            
            self.mem[address] = int(math.floor(div))
            return

        if action == 'mod':
            if self.mem[address] < 0 or secondArgVal <= 0:
                raise Exception('Modulo error')
            
            # modul = 
            # print('mod',self.mem[addresss],secondArgVal,modul)
            
            self.mem[address] = self.mem[address] % secondArgVal
            return
        if action == 'eql':
            eql = 0
            if self.mem[address] == secondArgVal:
                eql = 1
            self.mem[address] = eql
            return
        
        print('unknown command',intstruction)
        
    def runInput(self, address):
        # print()
        inputString = self.inputString[self.inputInd:self.inputInd+1]
        self.mem[address] = int(inputString)
        # print('input',address,self.mem[address], self)

        self.inputInd += 1

part_one_test('test.txt')
part_one('real.txt')
# part_two('test.txt')
part_two('real.txt')
