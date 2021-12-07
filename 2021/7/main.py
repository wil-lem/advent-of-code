import re
import time
import statistics

def part_one(file):
    start = time.time()
    crabs = read_file(file)
    med = int(statistics.median(crabs))
    print(med)
    fuel = 0
    for crab in crabs:
        fuel += abs(med-crab)
    print('P1 ' + file + ': ' + str(fuel))
    end = time.time()
    print("The time of execution of above program is :", round((end-start)*1000,3),'ms')

    
def part_two(file):
    start = time.time()
    grouped = []
    crabs = read_file(file)
    for crab in crabs:
        if len(grouped) <= crab:
            grouped += [0]*(crab-len(grouped) + 1)
        grouped[crab] += 1
    
    last = -1
    
    for inx,group in enumerate(grouped):
        fuel = getPositionScore(inx,grouped)
        if last > -1 and fuel > last:
            print(inx-1,last)
            break
        last = fuel

    print('P2 ' + file + ': ' + str(last))
    end = time.time()
    print("The time of execution of above program is :", round((end-start),3),'s')


def part_test():
    import random
    for i in range(0,100):
        randomlist = []
        for j in range(0,20):
            n = random.randint(0,10)
            randomlist.append(n)
        for j in range(0,10):
            n = random.randint(10,16)
            randomlist.append(n)
        
            
            
        grouped = []
        
        for crab in randomlist:
            if len(grouped) <= crab:
                grouped += [0]*(crab-len(grouped) + 1)
            grouped[crab] += 1
        
        last = -1
        
        for inx,group in enumerate(grouped):
            fuel = getPositionScore(inx,grouped)
            if last > -1 and fuel > last:
                break
            last = fuel
        if inx - 1 - round(statistics.mean(randomlist)) != 0:
            print(inx-1,statistics.mean(randomlist))




def getPositionScore(pos,groups):
    fuel = 0
    for inx,group in enumerate(groups):
        fuel += group*(pow(abs(pos-inx) + .5,2) - .25)/2
    return fuel;
      
def read_file(file):
    text_file = open("./input/" + file, "r")
    file_contents = text_file.read()
    lines = file_contents.splitlines()[0].split(',')

    return list(map(int, lines))
    
part_one('test.txt')
part_one('real.txt')
part_two('test.txt')
part_two('real.txt')
part_test()