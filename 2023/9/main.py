from numbersSequence import NumbersSequence

def getData(type='t', num=1):
    if type=='t':
        data = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""
    else:
        data=read_file('input.txt')
    return parseData(data)
    
def parseData(data):
    lines = data.splitlines()
    sequences = []
    for l in lines:
        sequences.append(NumbersSequence(l))
    
    return sequences

def part_one(type):
    seqs = getData(type)
    total = 0

    for seq in seqs:
        total += seq.getNext()
    
    return print('P1',str(total))

def part_two(type):
    seqs = getData(type)
    total = 0

    for seq in seqs:
        print(seq.numbers)
        print(seq.getPrev(),seq.numbers,seq.getNext())
        total += seq.getPrev()
    
    return print('P2',str(total))

def read_file(file):
    return open(file, "r").read()


    
part_one('t')
part_one('')
part_two('t')
part_two('')