import hand

class Hand:
    def __init__(self,line,useJokers):
        parts = line.split()
        
        self.hand = parts[0]
        self.bid = int(parts[1])
        self.score = -1
        self.useJokers = useJokers

    def getCardCounts(self):
        cardCounts = {}
        for i,c in enumerate(self.hand):
            if c not in cardCounts:
                cardCounts[c] = 0
            cardCounts[c] += 1
        return cardCounts

    def getScore(self):
        if self.score > -1:
            return self.score
        # We can give each hand a score based on it's relative strength
        # One pain = 2
        # Two pair = 3
        # 3 of a kind = 4
        # Full house = 5
        # 4 of a kind = 6
        # Five of a kind = 7
        # To compare similar hands we can use fractions
        # A =14, K=13, .... 2=2
        # For the first card  divide by 100, for the second 10,000, for the third 1,000,000
        handScore = 0
        for i,c in enumerate(self.hand):
            handScore += Hand.getCardNumber(c) / 10**(2*(i+1))
        
        cardCounts = self.getCardCounts()
        

        if self.isFiveOfAKind(cardCounts):
            self.score = handScore+7
            return self.score
        if self.isFourOfAKind(cardCounts):
            self.score = handScore+6
            return self.score
        if self.isFullHouse(cardCounts):
            self.score = handScore+5
            return self.score
        if self.isThreeOfAKind(cardCounts):
            self.score = handScore+4
            return self.score
        if self.isTwoPair(cardCounts):
            self.score = handScore+3
            return self.score
        if self.isOnePair(cardCounts):
            self.score = handScore+2
            return self.score
        self.score = handScore+1
        return self.score   
 
    def isFiveOfAKind(self, cardCounts):
        if len(cardCounts) == 1:
            return True
        if self.useJokers and len(cardCounts) == 2 and 'J' in cardCounts:
            return True
        return False
    
    def isFourOfAKind(self, cardCounts):
        for i in cardCounts:
            if cardCounts[i] == 4:
                return True
            if self.useJokers and i != 'J' and 'J' in cardCounts and cardCounts['J'] + cardCounts[i] == 4:
                return True
        
        return False
    
    def isFullHouse(self, cardCounts):
        if len(cardCounts) == 2:
            return True
        if self.useJokers and 'J' in cardCounts and len(cardCounts) == 3:
            return True
        return False
    
    def isThreeOfAKind(self, cardCounts):
        for i in cardCounts:
            if cardCounts[i] == 3:
                return True
            if self.useJokers and 'J' in cardCounts and cardCounts[i] == 2:
                return True
            
        return False
    
    def isTwoPair(self,cardCounts):
        # Any hand with a pair and a joker is automatically 3 of a kind
        # Any hand with 2 jokers is at least 3 of a kind
        # So we're done
        parts = 0
        for i in cardCounts:
            if cardCounts[i] == 2:
                if self.useJokers == False or i != 'J':
                    parts += 1
        if parts == 2:
            return True
        if parts == 1 and self.useJokers and 'J' in cardCounts:
            return True
        return False
        
        
    
    def isOnePair(self,cardCounts):
        if len(cardCounts) < 5:
            return True
        if self.useJokers and 'J' in cardCounts:
            return True
        return False 
        
    
    def getCardNumber(c):
        if c=='A':
            return 14
        if c=='K':
            return 13
        if c=='Q':
            return 12
        if c=='J':
            return 11
        if c=='T':
            return 10
        return int(c)
        
        
