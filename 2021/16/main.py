from enum import unique
from fractions import Fraction
import re
import statistics
import sys

def part_one(file):
    # map = read_file(file)
    # distance = map.findShortestPath()
    tests = [
        'D2FE28',
        '38006F45291200',
        'EE00D40C823060',
        '8A004A801A8002F478',
        '620080001611562C8802118E34',
        'C0015000016115A2E0802F182340',
        'A0016C880162017C3686B18A3D4780'
    ]


    for test in tests:
        packet = Packet(hex2bits(test),'')
        print('--',test,packet.getVersionSum())
        
    
    real = read_file('real.txt')
    packet = Packet(hex2bits(real),'')
    print('P1 test' + file + ': ' + str(packet.getVersionSum()))


def part_two(file):
        # map = read_file(file)
    # distance = map.findShortestPath()
    tests = [
        'C200B40A82',
        '04005AC33890',
        '880086C3E88112',
        'CE00C43D881120',
        'D8005AC2A8F0',
        'F600BC2D8F',
        '9C005AC2F8F0',
        '9C0141080250320F1802104A08'
    ]


    for test in tests:
        packet = Packet(hex2bits(test),'')
        print('--',test,packet.value)
        
    
    real = read_file('real.txt')
    packet = Packet(hex2bits(real),'')
    print('P2' + file + ': ' + str(packet.value))

class Packet:
    def __init__(self,completePacket,prefix):
        
        self.completeBits = completePacket
        self.version = int(self.completeBits[0:3],2)
        self.type = int(self.completeBits[3:6],2)
        self.children = []
        self.prefix = prefix
        
        if self.type == 4:
            self.value = int(self.getNumbers())
        else:
            self.parseChildren()
            self.value = int(self.calculateValue())

    def calculateValue(self):
        values = []
        for child in self.children:
            values.append(child.value)
        
        if self.type == 0:
            return sum(values)
        if self.type == 1:
            base = 1
            for val in values:
                base *= val
            return base
        if self.type == 2:
            return min(values)
        if self.type == 3:
            return max(values)
        if self.type == 5:
            if values[0] > values[1]:
                return 1
            return 0
        if self.type == 6:
            if values[0] < values[1]:
                return 1
            return 0
        if self.type == 7:
            if values[0] == values[1]:
                return 1
            return 0
        
        return False
        


    def parseChildren(self):
        self.lengthTypeID = self.completeBits[6:7]
        if self.lengthTypeID == '0':
            self.subPacketLength = int(self.completeBits[7:22],2)

            packets = self.completeBits[22:22+self.subPacketLength]
            while len(packets) > 0:
                p = Packet(packets, self.prefix+'   ')
                self.children.append(p)
                packets = p.remainder
            self.remainder = self.completeBits[22+self.subPacketLength:]
            
        else:
            self.subPacketLength = int(self.completeBits[7:18],2)
            
            packets = self.completeBits[18:]
            
            for i in range(0,self.subPacketLength):
                p = Packet(packets, self.prefix+'   ')
                self.children.append(p)
                packets = p.remainder
            
            self.remainder = packets

    

    def getNumbers(self):
        bytestring = self.completeBits[6:]
        resultByte = ''
        readDone = False
        count = 0
        while len(bytestring) >= 5:
            resultByte += bytestring[1:5]
            readDone = (bytestring[0:1] == '0')
            bytestring = bytestring[5:]
            count += 5
            if readDone:
                break
        self.remainder = self.completeBits[6+count:]
        return int(resultByte,2)

    def getVersionSum(self):
        version = self.version
        for pack in self.children:
            version += pack.getVersionSum()
        return version



def read_file(file):
    file_contents = open("./input/" + file, "r").read()
    # rows = []
    # map = Map()
    
    # for row,cols in enumerate(file_contents):
    #     for col,number in enumerate(cols):
    #         map.addPoint(Point(col,row,int(number)))
    # map.linkPoints()
    return file_contents
 
def hex2bits(hex):
    bitString = ''
    for i in hex:
        iVal = int(i,16)
        bitVal = bin(iVal)[2:]
        while len(bitVal) < 4:
            bitVal = '0' + bitVal
        bitString += bitVal
    return bitString

def getPacketVersion(byteString):
    version = byteString[:3]
    return int(version,2)

def getTypeId(byteString):
    type = byteString[3:6]
    return int(type,2)




    
part_one('test.txt')
# part_one('real.txt')
part_two('test.txt')
# part_two('real.txt')
