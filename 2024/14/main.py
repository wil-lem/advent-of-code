import re
import time
import math

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        pass

    # def add(self, v):
    #     self.x += v.x
    #     self.y += v.y
    #     pass

    def __str__(self):
        return 'Vector: ' + str(self.x) + ' ' + str(self.y)
    

class Robot:
    def __init__(self, x, y, vx, vy):
        self.p = Vector(x, y)
        self.v = Vector(vx, vy)
        self.above = []
        self.intervalY = 0

        self.pOriginal = Vector(x, y)

        self.inMiddleOffset = None
        self.inMiddleTiming = None

        self.time = 0
        pass

    def reset(self):
        self.p = Vector(self.pOriginal.x, self.pOriginal.y)
        self.time = 0
        pass

    def __str__(self):
        return 'Robot: ' + str(self.p.x) + ' ' + str(self.p.y) + ' ' + str(self.v.x) + ' ' + str(self.v.y)
        
    def getIsAboveOrBleow(self,t):
        t = t % self.interval.y
        
        if t == 0:
            t = self.interval.y
        # print(t,t in self.above, self.above)
        return t in self.lowOrHighY

    def getIsOnLeftorRight(self,t):
        t = t % self.interval.x
        
        if t == 0:
            t = self.interval.x
        # print(t,t in self.above, self.above)
        return t in self.lowOrHighX

    def computeAboveOrBelow(self,w,h):
        
        self.lowOrHighY = []
        self.lowOrHighX = []



        xLooped = False
        yLooped = False

        self.interval = Vector(0,0)

        backToOriginal = False
        t = 0
        while not backToOriginal:
            # Move and increase time
            t+=1
            self.move(1,w,h)
            if self.p.y < h/3 or self.p.y > 2*h/3:
                self.lowOrHighY.append(t)
            if self.p.x < w/h or self.p.x > 2*w/3:
                self.lowOrHighX.append(t)

            
            if self.p.x == self.pOriginal.x:
                xLooped = True
                self.interval.x = t

            if self.p.y == self.pOriginal.y:
                yLooped = True
                self.interval.y = t

            if xLooped and yLooped:
                backToOriginal = True
        self.reset()


    # def computeInMiddle(self,w,h):
    #     middle = Vector((w-1)/2,(h-1)/2)
        
    #     p = Vector(self.p.x,self.p.y)

    #     offset = Vector(-1,-1)
    #     interval = Vector(-1,-1)
    #     t = 0

    #     while offset.x == -1 or offset.y == -1 or interval.x == -1 or interval.y == -1:
    #         p.x = (p.x + self.v.x) % w
    #         p.y = (p.y + self.v.y) % h
    #         t += 1

    #         if p.x == middle.x:
    #             if offset.x == -1:
    #                 offset.x = t
    #             elif interval.x == -1:
    #                 interval.x = t - interval.x
    #         if p.y == middle.y:
    #             if offset.y == -1:
    #                 offset.y = t
    #             elif interval.y == -1:
    #                 interval.y = t - interval.y
    #     self.inMiddleOffset = offset
    #     self.inMiddleTiming = interval
        


    # def isInMiddle(self, axis, t):
    #     if axis == 'x':
    #         offset = self.inMiddleOffset.x
    #         interval = self.inMiddleTiming.x
    #     else:
    #         offset = self.inMiddleOffset.y
    #         interval = self.inMiddleTiming.y
        
    #     if t < offset:
    #         return False
        
    #     t -= offset
    #     if t < interval:
    #         return False
        
    #     return t % interval == 0

    # def getPosition(self,t):
    #     tV = Vector(t - self.inMiddleOffset.x) % self.inMiddleTiming.x, (t - self.inMiddleOffset.y) % self.inMiddleTiming.y
    #     p = Vector(self.p.original.x, self.p.original.y)
    #     p.x += tV.x * self.v.x
    #     p.y += tV.y * self.v.y
    #     return p
    


    def move(self, t, w, h):
        
        self.p.x += self.v.x * t
        self.p.y += self.v.y * t

        self.p.x = self.p.x % w
        self.p.y = self.p.y % h

        # middle = Vector((w-1)/2,(h-1)/2)
        # self.q = Vector(0,0)
        # if(self.p.x < middle.x):
        #     self.q.x = -1
        # elif(self.p.x > middle.x):
        #     self.q.x = 1
        # if(self.p.y < middle.y):
        #     self.q.y = -1
        # elif(self.p.y > middle.y):
        #     self.q.y = 1



        # return Vector(-1 if self.p.x < w/2 else 1, -1 if self.p.y < h/2 else 1)
    def getQuadrant(self):
        q = Vector(0,0)

        if(self.q.x == 0 or self.q.y == 0):
            return 0
        if(self.q.x == -1 and self.q.y == -1):
            return 1
        if(self.q.x == 1 and self.q.y == -1):
            return 2
        if(self.q.x == -1 and self.q.y == 1):
            return 3
        if(self.q.x == 1 and self.q.y == 1):
            return 4
        pass

    def getQ(self,t,w,h):
        p = Vector(self.pOriginal.x,self.pOriginal.y)
        p.x += self.v.x * t
        p.y += self.v.y * t
        p.x = p.x % w
        p.y = p.y % h
        return Vector(-1 if p.x < (w-1)/2 else 1, -1 if p.y < (h-1)/2 else 1)


        self.p.x = self.p.x % w
        self.p.y = self.p.y % h


def printMap(robots,w,h):
    countAbove = 0
    countLeft = 0
    for y in range(h):
        for x in range(w):
            count = 0
            for r in robots:
                if(r.p.x == x and r.p.y == y):
                    count += 1
                    if y < h/2:
                        countAbove += 1
                    if x < w/2:
                        countLeft += 1
            if count == 0:
                print(' ',end='')
            else:
                print(count,end='')
            
        print()
    print('above:',countAbove,'left:',countLeft)
    pass

def main(filename,w,h):
    lines = open('input/' + filename + '.txt').read().splitlines()
    robots=[]

    quadrants = {0:0,1:0,2:0,3:0,4:0}  
    for line in lines:
        matches = re.findall(r'([-\d]+)+', line)
        r = Robot(int(matches[0]), int(matches[1]), int(matches[2]), int(matches[3]))
        r.move(100, w, h)
        robots.append(r)
        
        quadrants[r.getQuadrant()] += 1

    total = quadrants[1] * quadrants[2] * quadrants[3] * quadrants[4]
    print('Total:',total)
    printMap(robots,w,h)

def main2(filename,w,h):
    
    lines = open('input/' + filename + '.txt').read().splitlines()

    robots=[]

    for line in lines:
        matches = re.findall(r'([-\d]+)+', line)
        r = Robot(int(matches[0]), int(matches[1]), int(matches[2]), int(matches[3]))
        r.computeAboveOrBelow(w,h)
        robots.append(r)
    
    size = 10000
    
    for t in range(0,size):
        yCount = 0
        xCount = 0
        for r in robots:
            yCount += 1 if r.getIsAboveOrBleow(t) else 0
            xCount += 1 if r.getIsOnLeftorRight(t) else 0
        # diff = abs(counts)
        if xCount < 90 and yCount < 160:
            for r in robots:
                
                r.move(t,w,h)
            
            printMap(robots,w,h)
            print('t:',t,'counts:',xCount, 'leftCount',yCount)
            # print('t%',h,t%h)
            print('-------------------')
            for r in robots:
                r.reset()
    
        
    
main('test',11,7)
main('real',101,103)

main2('real',101,103)