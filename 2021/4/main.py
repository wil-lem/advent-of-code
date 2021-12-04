import re

def part_one(file):
    lines = read_file(file)
    draws = []
    cards = []
    for line in lines:
        if(len(draws) == 0):
            draws = list(map(int,line.split(',')))
            continue
        if(line == ''):
            cards.append(BingoCard())
            continue

        cards[len(cards)-1].addRowString(line)

    wonCard = None
    for i in draws:
        for card in cards:
            if card.draw(int(i)):
                wonCard = card

        if wonCard:
            break
    print('P1 ' + file + ': ' + str(i * wonCard.sumUnmarked()))
            
def part_two(file):
    lines = read_file(file)
    draws = []
    cards = []
    for line in lines:
        if(len(draws) == 0):
            draws = list(map(int,line.split(',')))
            continue
        if(line == ''):
            cards.append(BingoCard())
            continue

        cards[len(cards)-1].addRowString(line)
    
    wonCardCount = 0
    wonCard = None

    for i in draws:
        for card in cards:
            if card.won:
                continue
            if card.draw(int(i)):
                wonCard = card
                wonCardCount += 1
        if(wonCardCount == len(cards)):
            break


    print('P2 ' + file + ': ' + str(i * wonCard.sumUnmarked()))
    
def read_file(file):
    text_file = open("./input/" + file, "r")
    file_contents = text_file.read()
    lines = file_contents.splitlines()

    # lines = list(map(bitsToDec,lines))

    # return list(map(int, lines))
    return lines

class BingoCard:
    
    
    def __init__(self):
        self.rows = []
        self.checkedRows = []
        self.won = False

    def draw(self, number):

        for row,cols in enumerate(self.rows):
            for col,val in enumerate(cols):
                if(number == val):
                    self.checkedRows[row][col] = True
        
        return self.cardWon()  
            
    def cardWon(self):
        if(self.won):
            return self.won

        checkedCols = [0]*5
        for row in self.checkedRows:
            if(sum(val for val in row) == len(row)):
                self.won = True
                break

            for col,val in enumerate(row):
                if val:
                    checkedCols[col] += 1
        
        if self.won == False:
            if 5 in checkedCols:
                self.won = True

        return self.won
        
    def sumUnmarked(self):
        total = 0
        for row,cols in enumerate(self.checkedRows):
            for col,val in enumerate(cols):
                if val == False:
                    total += self.rows[row][col]
        return total

    def addRowString(self, rowString):
        matches = re.findall('(\d+)', rowString)
        self.addRow(matches)
    def addRow(self, row):
        self.rows.append(list(map(int, row)))
        self.checkedRows.append([False]*len(row))


part_one('test.txt')
part_one('real.txt')
part_two('test.txt')
part_two('real.txt')