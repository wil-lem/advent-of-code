class MapLine:
    def __init__(self,line,y) -> None:
        self.line = line
        self.y = y
        self.numbers = []
        self.symbols = []
        
        for i,c in enumerate(line):
            if c.isdigit():
                if i == 0 or not line[i-1:i].isdigit():
                    l = 0
                    while len(line) >= i + l + 1 and line[i:i+l+1].isdigit():
                        l += 1
                    self.numbers.append(MapNumber(line[i:i+l],i,y))
            elif c != '.':
                self.symbols.append(MapSymbol(i,y,c))
    
    def getTouchingDigits(self,d):
        matches = []
        for n in self.numbers:
            if n.touchesSymbol(d):
                matches.append(n)
        return matches
    

class MapNumber:
    def __init__(self,number,x,y) -> None:
        self.number = number
        self.x = x
        self.y = y
    
    def touchesSymbol(self, symbol):
        # print('s',symbol.x,symbol.y)
        # print('d',self.number,self.x,self.y)

        dy = self.y - symbol.y
        if abs(dy) > 1:
            return False
        
        # print(symbol.x >= self.x - 1 and symbol.x <= self.x + len(self.number) + 1)
        # if dy == 0:
            # return (symbol.x + 1 == self.x or symbol.x == self.x + len(self.number))
        return (symbol.x >= self.x - 1 and symbol.x <= self.x + len(self.number))
    

        print(dy)

class MapSymbol:
    def __init__(self,x,y,c) -> None:
        self.x = x
        self.y = y
        self.gear = (c=='*')
