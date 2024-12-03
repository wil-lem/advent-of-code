import math

class Race:
    def __init__(self,t,d):
        self.t = t
        self.d = d
    
    def getHeldOptions(self):
        # Formula fo travel is:
        # Time button is held: x
        # RaceTime: t
        # RaceDistance: d
        # speed = x
        # distanceTraveled = DT = x(t-x)
        # DT = xt-x^2
        # x^2 - tx + DT = 0

        # Standard quadratic equation
        # ax²+bx+c=0
        # x = (-b ± √ (b²-4ac) ) / (2a) 
        # a=1
        # b = -t
        # c = DT

        # x = ( t ± √ (t² - 4 * self.t ) ) / 2 
        d = self.d + 1
        basePart = math.sqrt( self.t**2 - 4 * d )
        parts = [(self.t - basePart)/2,(self.t + basePart)/2]

        diff = math.floor(parts[1]) - math.ceil(parts[0]) + 1
        # print(parts)
        # print(diff)
        return diff
