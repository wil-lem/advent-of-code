from mapnumber import MapLine

def part_one(file):
    lines = read_file(file)
    numbers = []

    for i,line in enumerate(lines):
        for s in line.symbols:
            if i > 0:
                numbers += lines[i-1].getTouchingDigits(s)
            numbers += lines[i].getTouchingDigits(s)
            if i+1 <= len(lines):
                numbers += lines[i+1].getTouchingDigits(s)
    # return
    total = 0
    nNumbers = []
    for n in numbers:
        if n not in nNumbers:
            total += int(n.number)
            nNumbers.append(n)
    
    return print('P1 - ' + file + ': ' + str(total))

def part_two(file):
    lines = read_file(file)
    total = 0

    for i,line in enumerate(lines):
        for s in line.symbols:
            if s.gear:
                touching = []
                if i > 0:
                    touching += lines[i-1].getTouchingDigits(s)
                touching += lines[i].getTouchingDigits(s)
                if i+1 <= len(lines):
                    touching += lines[i+1].getTouchingDigits(s)
                
                if len(touching) == 2:
                    print(int(touching[0].number))
                    total += int(touching[0].number) * int(touching[1].number)

    return print('P2 - ' + file + ': ' + str(total))

def read_file(file):
    lines = open("./input/" + file, "r").read().splitlines()
    mapLines = []
    for i,line in enumerate(lines):
        mapLines.append(MapLine(line,i))
    return mapLines

part_one('test.txt')
part_one('real.txt')

part_two('test.txt')
part_two('real.txt')
