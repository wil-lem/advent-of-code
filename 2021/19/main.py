import re
import math
from typing import ChainMap


def part_one(file):
    scanners = read_file(file)
    mapScanners(scanners)
    
    points = []
    for scanner in scanners:
        # print('Gathering points for scanner',scanner.name)
        for probe in scanner.probes:
            p = probe.position
            if scanner.transform:
                p = p.applyTransform(scanner.transform)
            if str(p) not in points:
                points.append(str(p))
    
    
    return print('P1 - ' + file + ': ' + str(len(points)))

def part_two(file):
    scanners = read_file(file)
    mapScanners(scanners)

    maxDistance = 0
    for scanner in scanners:
        for scanner2 in scanners:
            dv = scanner.transform.offset.sub(scanner2.transform.offset)
            d = abs(dv.x) + abs(dv.y) + abs(dv.z)
            maxDistance = max(maxDistance,d)

    return print('P2 - ' + file + ': ' + str(maxDistance))

def mapScanners(scanners):

    scanners[0].transform = Transform.normal()
    
    
    while any( not x.transform for x in scanners):
        for scanner in list(filter(lambda x: not x.transform,scanners)):
            for scanner2 in list(filter(lambda x: x.transform,scanners)):
                scanner2.compareDistances(scanner)


def safeTr(matchingProbes):
    trs = []
    for i,m1 in enumerate(matchingProbes):
        for j,m2 in enumerate(matchingProbes):
            po1 = m1[0].position
            po2 = m2[0].position
            
            pt1 = m1[1].position
            pt2 = m2[1].position
            tr = Transform.compute(po1,po2,pt1,pt2)
            
            prevTr = False
            
            for otr in trs:
                if otr['trs'] == str(tr):
                    prevTr = otr
                    break
                    
            if prevTr:
                prevTr['count'] += 1
            else:
                trs.append({'tr':tr,'count':1,'trs':str(tr)})

        
    trs.sort(key=lambda x: x['count'],reverse=True)
    
    if trs[0]['count'] > 100:
        return trs[0]['tr']
    return False

def read_file(file):
    text_file = open("./input/" + file, "r").read().splitlines()
    
    scanners = []
    for line in text_file:
        m = re.match('-+ (.*?) -+',line)
        if m:
            scanner = Scanner(m[1])
            scanners.append(scanner)
            continue

        coords = line.split(',')
        if(len(coords) == 3):
            v = Vector(coords[0],coords[1],coords[2])
            p = Probe(v)
            scanners[-1].addProbe(p)

    return scanners

class Distance:
    def __init__(self, scanner, probe1, probe2):
        self.scanner = scanner
        self.probes = [probe1,probe2]
        self.distance = probe1.position.getDistance(probe2.position)
    
    def getMatchingProbes(self,distancePairs):
        probePairs = []
        for probe in self.probes:
            candidates = []
            for distancePair in distancePairs:
                if distancePair[0].probes[0] == probe:
                    candidates += distancePair[1].probes[:]
                if distancePair[0].probes[1] == probe:
                    candidates += distancePair[1].probes[:]

            bestCandidate = False
            bestCount = 0
            for candidate in candidates:
                if candidate == bestCandidate:
                    continue
                if candidates.count(candidate) > bestCount:
                    bestCandidate = candidate
                    bestCount = candidates.count(candidate)
            if bestCount > 1:
                probePairs.append([probe,bestCandidate])
        return probePairs



class Scanner:
    def __init__(self,name):
        self.name = name
        self.lines = []
        self.position = Vector(0,0,0)
        self.probes = []
        self.distances = False
        self.transform = False
        
    def addProbe(self,probe):
        self.probes.append(probe)

    def mapDistances(self):
        if self.distances:
            return
        
        self.distances = []
        for i,probe in enumerate(self.probes):
            for otherProbe in self.probes[i+1:]:
                distance = Distance(self,probe,otherProbe)
                self.distances.append(distance)

    def compareDistances(self,otherScanner):
        count = 0
        matchingProbes = []
        
        self.mapDistances()
        otherScanner.mapDistances()
        
        self.distances.sort(key=lambda a: a.distance)
        otherScanner.distances.sort(key=lambda a: a.distance)

        # The list will contain distance objects with same distance
        matchingDistancePairs = []
        for d in self.distances:
            equalDistances = list(filter(lambda od: od.distance == d.distance,otherScanner.distances))
            if len(equalDistances) == 1:
                matchingDistancePairs.append([d,equalDistances[0]])
            # if len(equalDistances) > 1:
            #     print('multipe matches')

        # The list should be filled with probe pairs that are the same probe but seen from different scanners
        matchingProbes = []
        for matchingPair in matchingDistancePairs:
            if any(x[0] in matchingPair[0].probes for x in matchingProbes):
                continue
            matchingProbes += matchingPair[0].getMatchingProbes(matchingDistancePairs)

        
        if len(matchingProbes) == 12:
            
            # po1 = matchingProbes[0][0].position
            # po2 = matchingProbes[1][0].position
            
            # pt1 = matchingProbes[0][1].position
            # pt2 = matchingProbes[1][1].position
            
            # tr = Transform.compute(po1,po2,pt1,pt2)
            tr = safeTr(matchingProbes)

            if not tr:

                # if not tr:
                print('False')
                return False

            if self.transform:
                # This scanner already has a transform
                # instead of setting the transform we found, figure out a transform that combines
                # this transform and the found transform
                
                p1 = Vector(-134,742524,1421)
                p2 = Vector(55,134,1924)
            
                pt1 = p1.applyTransform(tr)
                pt2 = p2.applyTransform(tr)
            
                pt1 = pt1.applyTransform(self.transform)
                pt2 = pt2.applyTransform(self.transform)
            
                trn = Transform.compute(pt1,pt2,p1,p2)
                otherScanner.transform = trn

                # print('Setting mod transform', self.name, '->', otherScanner.name)

            else:
                # print('Setting transform', self.name, '->', otherScanner.name)
                
                otherScanner.transform = tr

            
            
            return True


        return False

class Probe:
    def __init__(self, v):
        self.position = v
        self.clones = []
        self.distances = False

    def addClone(self,probe):
        if probe not in self.clones:
            self.clones.append(probe)
        if self not in probe.clones:
            probe.clones.append(self)

    def print(self):
        print('Probe')
        self.position.print()


class Vector:
    def __init__(self,x,y,z):
        self.x = int(x)
        self.y = int(y)
        self.z = int(z)

    def getDistance(self,other):
        return math.sqrt( pow(self.x - other.x,2) + pow(self.y - other.y,2) + pow(self.z - other.z,2))
        
    def getSelfDistance(self):
        other = Vector(0,0,0)
        return self.getDistance(other)

    def print(self):
        print(self.x,self.y,self.z)

    def clone(self):
        return Vector(self.x,self.y,self.z)

    def sub(self,other):
        v = self.clone()
        v.x -= other.x
        v.y -= other.y
        v.z -= other.z
        return v

    def abs(self):
        v = self.clone()
        v.x = abs(v.x)
        v.y = abs(v.y)
        v.z = abs(v.z)
        return v
    
    def eq(self,other):
        return self.x == other.x and self.y == other.y and self.z == other.z
    
    def __str__(self) -> str:
        return str(self.x) + ',' + str(self.y) + ',' + str(self.z)

    def getTransformVector(val,targetVector):
        targetVectorAbs = targetVector.abs()
        if targetVectorAbs.x == abs(val):
            if targetVector.x == val:
                return Vector(1,0,0)
            else:
                return Vector(-1,0,0)
        if targetVectorAbs.y == abs(val):
            if targetVector.y == val:
                return Vector(0,1,0)
            else:
                return Vector(0,-1,0)
        if targetVectorAbs.z == abs(val):
            if targetVector.z == val:
                return Vector(0,0,1)
            else:
                return Vector(0,0,-1)
        return False
    
    def applyTransform(self,tr):
        nv = Vector(
            self.x * tr.x.x + self.y * tr.x.y + self.z * tr.x.z, 
            self.x * tr.y.x + self.y * tr.y.y + self.z * tr.y.z, 
            self.x * tr.z.x + self.y * tr.z.y + self.z * tr.z.z, 
        )
        nv.x += tr.offset.x
        nv.y += tr.offset.y
        nv.z += tr.offset.z
        return nv

class Transform:
    def __init__(self):
        self.x = None
        self.y = None
        self.z = None
        self.offset = None
    
    def normal():
        tr = Transform()
        tr.x = Vector(1,0,0)
        tr.y = Vector(0,1,0)
        tr.z = Vector(0,0,1)
        tr.offset = Vector(0,0,0)
        return tr

    def compute(po1, po2, pt1, pt2):
        do = po1.sub(po2)
        dt = pt1.sub(pt2)
        doa = do.abs()
        
        if doa.x == doa.y or doa.x == doa.z or doa.y == doa.z:
            return False
        
        tr = Transform()
        tr.x = Vector.getTransformVector(do.x,dt)
        tr.y = Vector.getTransformVector(do.y,dt)
        tr.z = Vector.getTransformVector(do.z,dt)
        
        if not tr.x or not tr.y or not tr.z:
            return False
        
        #Todo, check if transforms share a coordinate
        
        tr.offset = Vector(0,0,0)

        pt1t = pt1.applyTransform(tr)
        pt2t = pt2.applyTransform(tr)
        
        # We still don't know it po1 matches pt1 or pt2, but we need to know it to find the offset
        dtest1 = pt1t.sub(pt2t)
        dtest2 = pt2t.sub(pt1t)
        if dtest1.eq(do):
            diff = po1.sub(pt1t)
            tr.offset = diff 
            pt1final = pt1.applyTransform(tr) 
            if pt1final.eq(po1):
                return tr
            
        
        elif dtest2.eq(do):
            tr.offset = po1.sub(pt2t)
            ptfinal = pt2.applyTransform(tr) 
            if ptfinal.eq(po1):
                return tr
    
        return False

    def print(self):
        print('tr')
        if self.x:
            print(' x:',self.x.x,self.x.y,self.x.z)
        else:
            print(' x: none')
        if self.y:
            print(' y:',self.y.x,self.y.y,self.y.z)
        else:
            print(' y: none')
        if self.z:
            print(' z:',self.z.x,self.z.y,self.z.z)
        else:
            print(' z: none')
        if self.offset:
            print(' o:',self.offset.x,self.offset.y,self.offset.z)
        else:
            print(' o: none')
    
    def __str__(self) -> str:
        return 'x:('+str(self.x)+')y:('+str(self.x)+')z:('+str(self.x)+')o:'+str(self.offset)
            


def get_intersections(x0, y0, r0, x1, y1, r1):
    # circle 1: (x0, y0), radius r0
    # circle 2: (x1, y1), radius r1

    d=math.sqrt((x1-x0)**2 + (y1-y0)**2)
    
    # non intersecting
    if d > r0 + r1 :
        return None
    # One circle within other
    if d < abs(r0-r1):
        return None
    # coincident circles
    if d == 0 and r0 == r1:
        return None
    else:
        a=(r0**2-r1**2+d**2)/(2*d)
        h=math.sqrt(r0**2-a**2)
        x2=x0+a*(x1-x0)/d   
        y2=y0+a*(y1-y0)/d   
        x3=x2+h*(y1-y0)/d     
        y3=y2-h*(x1-x0)/d 

        x4=x2-h*(y1-y0)/d
        y4=y2+h*(x1-x0)/d
        
        return (x3, y3, x4, y4)

part_one('test.txt')
part_one('real.txt')

part_two('test.txt')
part_two('real.txt')