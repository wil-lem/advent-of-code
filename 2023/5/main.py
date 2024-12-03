from conversionMap import ConversionMap
from conversionMap import NumberRange

def part_one(file):
    data = read_file(file)

    minN = -1
    for n in map(int,data['seeds']):
        
        for m in data['maps']:
            n = m.convert(n)
        if minN < 0:
            minN = n
        else:
            minN = min(minN,n)
   
    return print('P1 - ' + file + ': ' + str(minN))

def part_two(file):
    data = read_file(file)

    minN = -1
    for i in range(0,int(len(data['seeds'])/2)):
        seedStart = int(data['seeds'][i*2])
        seedLength = int(data['seeds'][i*2+1])
        seedRange = NumberRange(seedStart, seedLength-1)
        
        results = [seedRange]
        for m in data['maps']:
            results = m.convertRanges(results)

        for r in results:
            if minN < 0:
                minN = r.start
            else:
                minN = min(r.start,minN)


    
    return print('P2 - ' + file + ': ' + str(minN))

def read_file(file):
    lines = open("./input/" + file, "r").read().splitlines()
    maps = []
    seeds = list(filter(None,lines[0].split(':')[1].split(' ')))

    mapLines = []
    for line in lines[2:] + ['']:
        if line != '':
            mapLines.append(line)
        else:
            maps.append(ConversionMap(mapLines))
            mapLines = []
    return {"seeds":seeds,"maps":maps}
    


    
part_one('test.txt')
part_one('real.txt')

part_two('test.txt')
part_two('real.txt')
