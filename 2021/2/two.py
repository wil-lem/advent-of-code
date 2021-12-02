import re


def part_one(file):
    
    lines = read_file(file)
    x = 0
    y = 0
    
    for line in lines:
        m = re.match(r"(?P<direction>\w+) (?P<distance>\d+)", line)
        if m:
            dist = int(m.group('distance'));
            if(m.group('direction') == 'forward'):
                x += dist
            elif(m.group('direction') == 'up'):
                y -= dist
            elif(m.group('direction') == 'down'):
                y += dist
            
    print('Part one - ' + file + ': ' + str(x*y))


def part_two(file):
    
    lines = read_file(file)
    x = 0
    y = 0
    aim = 0
    
    for line in lines:
        m = re.match(r"(?P<direction>\w+) (?P<distance>\d+)", line)
        if m:
            dist = int(m.group('distance'));
            if(m.group('direction') == 'forward'):
                x += dist
                y += dist * aim
            elif(m.group('direction') == 'up'):
                aim -= dist
            elif(m.group('direction') == 'down'):
                aim += dist
            
    print('Part two - ' + file + ': ' + str(x*y))
        

def read_file(file):
    text_file = open("./input/" + file, "r")
    file_contents = text_file.read()
    lines = file_contents.splitlines()
    # return list(map(int, lines))
    return lines

part_one('test.txt')
part_one('real.txt')
part_two('test.txt')
part_two('real.txt')