from hand import Hand

def part_one(file):
    hands = read_file(file)
    hands.sort(key=lambda h: h.getScore())

    total = 0
    for i,h in enumerate(hands):
        total += h.bid * (i+1)
    

    return print('P1 - ' + file + ': ' + str(total))

def part_two(file):
    hands = read_file(file, True)
    hands.sort(key=lambda h: h.getScore())

    total = 0
    for i,h in enumerate(hands):
        total += h.bid * (i+1)
    # hands = ['12345 1']

    # for h in hands:
    #     hand = Hand(h, True)
    #     print(h, hand.isOnePair(hand.getCardCounts()))
    #     print(hand.getCardCounts())

    return print('P2 - ' + file + ': ' + str(total))

def read_file(file, useJokers = False):
    lines = open("./input/" + file, "r").read().splitlines()
    
    hands = []
    for l in lines:
        hands.append(Hand(l,useJokers))

    return hands



    
part_one('test.txt')
part_one('real.txt')

part_two('test.txt')
part_two('real.txt')
