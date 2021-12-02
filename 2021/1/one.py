

def part_one(file):
    
    lines = read_file(file)
    prev=False
    larger=0

    for curr in lines:
        if prev != False:
            if curr > prev:
                larger += 1
        prev = curr

    print('Part one - ' + file + ': ' + str(larger))
    
def part_two(file):
    lines = read_file(file)
    increased = 0

    for idx, val in enumerate(lines[3:]):
        shared = lines[idx + 1] + lines[idx + 2]
        curr =  shared + val
        prev = lines[idx] + shared
        if prev != False:
            if curr > prev:
                increased += 1

    print('Part two - ' + file + ': ' + str(increased))
        

def read_file(file):
    text_file = open("./input/" + file, "r")
    file_contents = text_file.read()
    lines = file_contents.splitlines()
    return list(map(int, lines))

part_one('test.txt')
part_one('real.txt')
part_two('test.txt')
part_two('real.txt')