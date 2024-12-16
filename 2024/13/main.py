import re
import time
import math

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.considerMax = True
        pass

    def __string__(self):
        return f'({self.x},{self.y})'
    
    def slope(self):
        return self.y/self.x
    
    def angle(self):
        # We kinda assume all vectors start at 0,0 and x and y are positive
        return math.atan(self.slope())
    
    def distanceZero(self):
        return math.sqrt(self.x**2 + self.y**2)
    
    def add(self, vector):
        return Vector(self.x + vector.x, self.y + vector.y)
    
    def abs(self):
        return Vector(abs(self.x), abs(self.y))
    
    def multiply(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)
        
class Machine:
    def __init__(self): 
        self.buttons = {}
        self.prize = Vector(0, 0)
        pass

    def addButton(self, button):
        results = re.findall(r"Button ([A-Z]).*?(\d+).*?(\d+)", button)
        self.buttons[results[0][0]] = Vector(int(results[0][1]), int(results[0][2]))

    def addPrize(self, prize):
        results = re.findall(r"Prize.*?(\d+).*?(\d+)", prize)
        self.prize = Vector(int(results[0][0]), int(results[0][1]))

    def cheapestRouteToPrize(self):
        costA = 3
        costB = 1
        
        # We have a triangle with three sides.
        # We'll use these variables
        
        # dA = the distance covered by button A
        # dB = the distance covered by button B
        # dP = the distance to the prize
        # aA = the angle oppostite to dA
        # aB = the angle opposite to dB
        # aP = the angle opposite to dP
        dP = self.prize.distanceZero()
        
        aB = self.prize.angle() - self.buttons['A'].angle()
        aP = math.pi - self.buttons['B'].angle() + self.buttons['A'].angle()
        
        
        # use the sine rule to find the distance covered by button B
        # dP/sin(aP) = dB/sin(aB)
        dB = dP * math.sin(aB) / math.sin(aP)

        stepsB = round(dB / self.buttons['B'].distanceZero())
        stepsA = round((self.prize.x - (stepsB * self.buttons['B'].x)) / self.buttons['A'].x)
        
        distanceA = self.buttons['A'].multiply(stepsA * -1)
        distanceB = self.buttons['B'].multiply(stepsB * -1)
        distanceCheck = self.prize.add(distanceA).add(distanceB).abs()

        if(distanceCheck.distanceZero() > 0.000001):
            return False
        
        return (stepsA * costA) + (stepsB * costB)

    def __string__(self):
        return f'Buttons: A {self.buttons["A"].__string__()} B {self.buttons["B"].__string__()} Prize: {self.prize.__string__()}'
    
def main(filename):
    machines = []
    lines = open('input/' + filename + '.txt').read().splitlines()
    for line in lines:
        if re.match(r"Button A", line):
            machines.append(Machine())
            machines[-1:][0].addButton(line)
        elif re.match(r"Button B", line):
            machines[-1:][0].addButton(line)
        elif re.match(r"Prize", line):
            machines[-1:][0].addPrize(line)

    totalCost = 0
    for machine in machines:        
        cost = machine.cheapestRouteToPrize()
        if cost:
            totalCost += cost
    print(int(totalCost))
    
    totalCost = 0
    count = 0
    for machine in machines:
        machine.prize.x += 10000000000000
        machine.prize.y += 10000000000000
        machine.considerMax = False
        cost = machine.cheapestRouteToPrize()
        if cost:
            count += 1
            totalCost += cost
        # print(machine.__string__())
    print(str(totalCost) + ' (' + str(count) + ')')
main('test')
main('real')