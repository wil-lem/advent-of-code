
class NumbersSequence:
    def __init__(self,line):
        self.numbers = list(map(int,line.split()))
        self.child = False
        
    def buildChildren(self):
        if len(list(filter(lambda n: n!=0,self.numbers))) == 0:
            return False
        self.child = NumbersSequence.fromParent(self.numbers)
        

    def getNext(self):
        self.buildChildren()
        
        if self.child == False:
            return 0
        return self.numbers[-1] + self.child.getNext()
        
    def getPrev(self):
        self.buildChildren()
        
        if self.child == False:
            return 0
        return self.numbers[0] - self.child.getPrev()

    def fromParent(numbers):
        seq = NumbersSequence('')
        for i,n in enumerate(numbers[:-1]):
            seq.numbers.append(numbers[i+1] - n)
        return seq