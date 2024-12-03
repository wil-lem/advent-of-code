from race import Race

def part_one(file):
    data = read_file(file)
    total = 1
    for r in data:
        total *= r.getHeldOptions()

    return print('P1 - ' + file + ': ' + str(total))

def part_two(file):
    data = read_file_two(file)

    total = data.getHeldOptions()
    
    return print('P2 - ' + file + ': ' + str(total))

def read_file(file):
    lines = open("./input/" + file, "r").read().splitlines()
    times = list(map(int,lines[0].split()[1:]))
    distance = list(map(int,lines[1].split()[1:]))
    
    races = []
    for i,t in enumerate(times):
        races.append(Race(t,distance[i]))

    return races

def read_file_two(file):
    lines = open("./input/" + file, "r").read().splitlines()
    times = lines[0].split()[1:]
    distance = lines[1].split()[1:]
    
    t = int(''.join(lines[0].split()[1:]))
    d = int(''.join(lines[1].split()[1:]))
    
    return Race(t,d)



    
part_one('test.txt')
part_one('real.txt')

part_two('test.txt')
part_two('real.txt')
