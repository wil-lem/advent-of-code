import re

def part_one(file):
    count = runDays(file,80)
    print('P1 ' + file + ': ' + str(count))
    
def part_two(file):
    count = runDays(file,256)
    print('P2 ' + file + ': ' + str(count))
    

def runDays(file,days):
    
    lines = read_file(file)
    fishCount = [0]*9

    for age in lines:
        fishCount[age] += 1
    
    day = 0
    
    while day < days:
        ageZero = fishCount[0]
        fishCount = fishCount[1:]
        fishCount[6] += ageZero
        fishCount.append(ageZero)
        
        day += 1
    return sum(fishCount)

      
def read_file(file):
    text_file = open("./input/" + file, "r")
    file_contents = text_file.read()
    lines = file_contents.splitlines()[0].split(',')

    return list(map(int, lines))
    
part_one('test.txt')
part_one('real.txt')
part_two('test.txt')
part_two('real.txt')