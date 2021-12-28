from enum import unique
from fractions import Fraction
import re
import statistics
import sys
import math

def part_one(file):
    coords = read_file(file)

    # Formula for y
    # vys = y start speed
    # n = step number
    # say we have vy is 1: n0=>y0, n1=>y1, n2=>y1, n3=>y0, n4=>y-2
    # or vy=-1: n0=>y0, n1=>-1, n2=>-3, n3=>-6
    # y = -.5n² + (vys + .5)n
    #
    # Formulate for x
    # vxs = x start speed
    # say we have vx is 1: n0=>y0, n1=>x1, n2=>x1, n3=>x1, n4=>x1
    # or vx=2: n0=>0, n1=>2, n2=>3, n3=>3
    # vx=3: n0=>0, n1=>3, n2=>5, n3=>6, n3=>6
    # x = n*vx - n(n-1)/2
    # x = n*vx - (n² - n)/2
    # x = n*vx - .5n² + .5n
    # x = n*vx - .5n² + .5n
    # x = -.5n² + n*vx + .5n
    # x = -.5n² + n(vx + .5)

    # Extra rule, if n>vx -> n=vx
    



    # For y:
    # s1: y=vys
    # s2: y= vys + (vys - 1)
    # s3: y= vys + (vys - 1) + (vys - 2) = 3 * vys - 2
    # sn: y = n * vys - n(n-1)/2
    # y = n * vys - n² / 2 + n/2
    # y = -.5n² + (vys + .5)n

    # The callenge for y is the following, say we start with vys = 1
    # That means that after 2 turns, vys will be -1 and the probe will be at height 0
    # At vys = 1, n=3, y=0, vy=-2
    # At vys = 2, n=5, y=0, vy=-3
    # At vys = 3, n=7, y=0, vy=-4
    # This means at the next step ( s = vys * 2 + 2 ) y will be vys - 1 
    # Thus to this the maximum vys we have to hit the bottom of the area witht the next step
    # ymin = -1 * vys - 1
    # ymin + 1 = -1*vys
    # -1*ymin - 1 = vys
    
    # The step that we will be at the highest point is equal to vys
    #
    # So we have:
    # y = -.5n² + (vys + .5)n
    # vys = -1*ymin - 1
    # n = vys
    # 
    # We get:
    # y = -.5(-ymin - 1)² + ((-ymin - 1) + .5)(-ymin - 1)
    # y = -.5(ymin²+2ymin+1) + (-ymin - .5)(-ymin - 1)
    # y = -.5ymin² - ymin - .5 + ymin² + ymin + .5ymin + .5
    # y = .5ymin² + .5ymin
    #
    
    ymin = coords['min']['y']
    y = .5 * pow(ymin,2) + .5*ymin

    print('P1 ' + file + ': ' + str(y))

def part_two(file):
    coords = read_file(file)

    # Start by figuring out the ranges for x and y:
    vymin = coords['min']['y']
    vymax = -1*coords['min']['y']
    
    # To get xmin we have to know the formula for the slope of x
    # x = -.5n² + (vxs+.5)n
    # x' = -n + vxs + .5
    # If slope is zero
    # 0 = -n + vxs + .5
    # n = vxs + .5
    #
    # We can plug that into the genral x function
    # x = -.5(vxs + .5)² + (vxs+.5)(vxs+.5)
    # x = -.5(vxs + .5)² + (vxs+.5)²
    # x = .5(vxs + .5)²    
    # We want to know vxs, not x
    # 2x = (vxs + .5)²
    # ±√(2x) = vxs + .5
    # vxs = ±√(2x) - .5
    vxmin = math.ceil(math.sqrt(2*coords['min']['x']) - .5)
    
    #Max vx is equal to max x
    vxmax =  coords['max']['x']
    
    coordsResults = []

    for vy in range(vymin,vymax+1):

        steps = []
        for y in range(coords['min']['y'],coords['max']['y'] + 1):
            
            # We want to know the step for each y coordinate
            # y = -.5n² + (vys + .5)n
            # -2y = n² - 2n(vys + .5) + (vys + .5)² - (vys + .5)²
            # (vys + .5)² - 2y = (n - (vys + .5))²
            # ±√( (vys + .5)² - 2y ) = n - vys - .5
            # ±√((vys + .5)² - 2y) + vys + .5 = n
            # ±√(vys² + vys + .25 - 2y) + vys + .5 = n
            rootPart = pow(vy,2) + vy + .25 - 2*y
            if rootPart < 0:
                continue
            # We'll just ignore the negative values
            n = math.sqrt(rootPart) + vy + .5
            
            if (n - math.floor(n) == 0):
                steps.append(n)

        if(len(steps) < 1):
            continue

        # Now we know at what steps a given value of vy will have a proper value for y
        # now check the xvalues for all these steps.
        # x = -.5n² + n(vx + .5)
        for vx in range(vxmin,vxmax+1):
            for n in steps:

                # the x formula flips at some point, if we reacht that point, treat the step as the last
                # step before the flip
                xn = n
                if xn >= vx + .5:
                    xn = vx
                
                x = -.5 * pow(xn,2) + (vx +.5) * xn
                if x >= coords['min']['x'] and x <= coords['max']['x']: 
                    coord = str(vx) + ',' + str(vy)
                    if coord not in coordsResults:
                        coordsResults.append(coord)
                    
    print('P2 ' + file + ': ' + str(len(coordsResults)))

    
def read_file(file):
    file_contents = open("./input/" + file, "r").read()
    search = re.findall('(-{0,1}\d+)',file_contents)
    
    return {
        "min": {
            "x": int(search[0]),
            "y": int(search[2])
        },
        "max": {
            "x": int(search[1]),
            "y": int(search[3])
        }
    }
    
            
    
part_one('test.txt')
part_one('real.txt')
part_two('test.txt')
part_two('real.txt')
