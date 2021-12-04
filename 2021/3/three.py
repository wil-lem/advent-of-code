import re



def part_one(file):
    lines = read_file(file)
    size = byte_size(file)
    indexes = [0]*size
    
    for line in lines:
        i = size - 1
        while i >= 0:
            if line >= pow(2,i):
                indexes[i] += 1
                line -= pow(2,i)
            i -= 1

    gamma = 0
    epsilon = 0
    
    for inx,val in enumerate(indexes):
        if val > len(lines)/2:
            gamma += pow(2,inx)
        else:
            epsilon += pow(2,inx)
    
    return print('P1 - ' + file + ': ' + str(gamma * epsilon))

def part_two(file):
    byteSize = byte_size(file)
    mainList = read_file(file)
    oxRefList = [True]*len(mainList)
    co2RefList = [True]*len(mainList)
    
    i = int(byteSize)
    while i > 0 and sum(useInx for useInx in oxRefList) > 1:
        oxRefList = parseBits(mainList,oxRefList,i,byteSize,True)
        i -= 1
    i = int(byteSize)
    while i > 0 and sum(useInx for useInx in co2RefList) > 1:
        co2RefList = parseBits(mainList,co2RefList,i,byteSize,False)
        i -= 1
    

    solution = mainList[oxRefList.index(True)] * mainList[co2RefList.index(True)]
    print('P2 - ' + file + ': ' + str(solution))
    
    
def parseBits(baseList,selectedIndexes,power,byteSize,searchBiggest):
    higherIndexes = []
    lowerIndexes = []
    for inx,useInx in enumerate(selectedIndexes):
        if(useInx):
            if(stripValOfHigherBits(baseList[inx],power,byteSize) >= pow(2,power-1)):
                higherIndexes.append(inx)
            else:
                lowerIndexes.append(inx);    
    
    selectedIndexes = [False]*len(baseList)

    if(searchBiggest):
        if(len(higherIndexes) >= len(lowerIndexes)):
            for inx in higherIndexes:
                selectedIndexes[inx] = True;
        else:
            for inx in lowerIndexes:
                selectedIndexes[inx] = True;
    else:
        if(len(lowerIndexes) <= len(higherIndexes)):
            for inx in lowerIndexes:
                selectedIndexes[inx] = True;
        else:
            for inx in higherIndexes:
                selectedIndexes[inx] = True;
        
    return selectedIndexes

def stripValOfHigherBits(val,power,byteSize):
    while power < byteSize:
        byteSize -= 1;  
        if val >= pow(2,byteSize):
            val -= pow(2,byteSize)
    return val

def byte_size(file):
    text_file = open("./input/" + file, "r")
    file_contents = text_file.read()
    lines = file_contents.splitlines()
    return len(lines[0])

def read_file(file):
    text_file = open("./input/" + file, "r")
    file_contents = text_file.read()
    lines = file_contents.splitlines()

    lines = list(map(bitsToDec,lines))

    # return list(map(int, lines))
    return lines

def bitsToDec(byte):
    num = 0
    i = len(byte) - 1
    for bit in byte:
        num += int(bit) * pow(2,i)
        i -= 1
    
    return num

    #This would also work
    #return int(byte,2)

part_one('test.txt')
part_one('real.txt')
part_two('test.txt')
part_two('real.txt')