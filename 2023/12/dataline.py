variantsCache = {}

class DataLine:
    def __init__(self,line):
        parts = line.split(' ')
        # Numbers are the the options we need to fir to the map
        self.numbers = list(map(int,parts[1].split(',')))
        # The map is de line describing where lava might be/is.
        # we don't really need it but we'll save it for now
        self.map = parts[0]

        # use the map to identify some blocks where lava migh be
        self.blocks = []
        variantPaths = {"start":[1,self.numbers]}
        for blockMap in parts[0].split('.'):
            if blockMap != '':
                block = Block(blockMap)
                self.blocks.append(block)

        for b in self.blocks:
            # Get new variantspaths
            newVariantPaths = {}
            for vp in variantPaths:
                variantPath = variantPaths[vp]
                multiplier = variantPaths[vp][0]
                vvariants = b.getVariants(variantPath[1])
                for v in vvariants:
                    count = vvariants[v][0]*multiplier
                    if v in newVariantPaths:
                        newVariantPaths[v][0] += count
                    else:
                        newVariantPaths[v] = vvariants[v]
                        newVariantPaths[v][0] = count
            
            variantPaths = newVariantPaths
            
        self.total = variantPaths['k'][0]


                

class Block:
    def __init__(self,map) -> None:
        self.map = map
        self.questionMarks = []
        
        
    # This function should walks through all options in the map to see how we can match it
    def getVariants(self, numbers):
        
        # Create a cache key with the map object and the first few relavant numbers
        ckey = 'c-' + self.map + '-'
        
        lenCount = -1
        for i,n in enumerate(numbers):
            if lenCount <= len(self.map):
               lenCount += n + 1
               ckey += '-' + str(n)
        print(len(variantsCache))
        print(ckey)
        
        if ckey in variantsCache:
            variants = variantsCache[ckey]
        else:
            variants = self.generateVariants(numbers)
            variantsCache[ckey] = variants

        uniqueVariants = {}
        for v in variants:
            mapNumbers = Block.getMapNumbers(v)
            leftNumbers = numbers[len(mapNumbers):]
            dKey = 'k' + '-'.join(map(str,leftNumbers))
            if dKey in uniqueVariants:
                uniqueVariants[dKey][0] += 1
            else:
                uniqueVariants[dKey] = [1,leftNumbers,mapNumbers]
        return uniqueVariants

    def generateVariants(self,numbers):
        variants = ['']
        leftNumers = numbers[:]

        for i,c in enumerate(self.map):
            newVariants = []
            for v in variants:
                if c == '#':
                    appendString = ''
                    while leftNumers[0] > len(appendString):
                        appendString

                    newVariants.append(v+'#')
                else:
                    newVariants.append(v+'.')
                    newVariants.append(v+'#')
            variants = []
            for v in newVariants:
                if Block.validMap(v,numbers, i+1 == len(self.map)):
                    variants.append(v)
        return variants

    def validMap(aMap,numbers, lastMustMatch):
        # numbers 3,2,1
        # valid ..###..##.#
        
        # nMap = list(map(len,['addcd','a']))
        nMap = Block.getMapNumbers(aMap)
        if len(nMap) > len(numbers):
            return False
        for i,n in enumerate(nMap):
            if lastMustMatch or i+1 < len(nMap):
                if n != numbers[i]:
                    return False
            else:
                if n > numbers[i]:
                    return False
          
        return True

    def getMapNumbers(aMap):
        return list(map(len,filter(None,aMap.split('.'))))

