from ticket import Ticket

def part_one(file):
    tickets = read_file(file)

    total = 0
    for t in tickets:
        total += t.score
    
    return print('P1 - ' + file + ': ' + str(total))

def part_two(file):
    tickets = read_file(file)

    total = 0
    for i,t in enumerate(tickets):
        total += t.copies
        c = t.matchCount
        while c > 0:
            tickets[i+c].copies += t.copies
            c -= 1

    return print('P2 - ' + file + ': ' + str(total))

def read_file(file):
    lines = open("./input/" + file, "r").read().splitlines()
    tickets = []
    for line in lines:
        tickets.append(Ticket(line))
    return tickets

part_one('test.txt')
part_one('real.txt')

part_two('test.txt')
part_two('real.txt')
