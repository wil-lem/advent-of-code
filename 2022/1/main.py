from enum import unique
import re
import statistics

def part_one(file):

    lines = read_file(file)
    lines.append('')

    elf_calroies=0
    max_calories=0
    for calories in lines:
        if calories != '':
            elf_calroies+=int(calories)
        else:
            if elf_calroies > max_calories:
                max_calories = elf_calroies
            elf_calroies = 0

    
    print(max_calories)

    # print('P1 ' + file + ': ' + str(count))
    
    
def part_two(file):
    lines = read_file(file)
    lines.append('')
    elves = []
    elf = 0
    for calories in lines:
        if calories != '':
            elf+=int(calories)
        else:
            elves.append(elf)
            elf = 0
    elves.sort()
    print(sum(elves[-3:]))

def read_file(file):
    return open("./input/" + file, "r").read().splitlines()
    
    
part_one('test.txt')
part_one('real.txt')
part_two('test.txt')
part_two('real.txt')