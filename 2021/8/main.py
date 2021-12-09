from enum import unique
import re
import statistics

def part_one(file):
    data = read_file(file)
    uniqueCount = 0
    unigueLengths = [2,4,3,7]
    for line in data:
        for digit in line[1]:
            if len(digit) in unigueLengths:
                uniqueCount += 1
                
        
    print('P1 ' + file + ': ' + str(uniqueCount))
    
    
def part_two(file):
    data = read_file(file)

    solution = 0

    for line in data:
        solution += readNumber(line[0],line[1])    
        # break
    
    print('P2 ' + file + ': ' + str(solution))

def readNumber(testInputs, numberInputs):
    baseMap = ['a','b','c','d','e','f','g']
    
    # Map which wires are on for which numbers
    filterMap = [
        ['a','b','c','e','f','g'],      # 0 - 6
        ['c','f'],                      # 1 - 2
        ['a','c','d','e','g'],          # 2 - 5
        ['a','c','d','f','g'],          # 3 - 5
        ['b','c','d','f'],              # 4 - 4
        ['a','b','d','f','g'],          # 5 - 5
        ['a','b','d','e','f','g'],      # 6 - 6
        ['a','c','f'],                  # 7 - 3
        ['a','b','c','d','e','f','g'],  # 8 - 8 
        ['a','b','c','d','f','g'],      # 9 - 6
    ]

    # Every wire will get a map of possible connections so a:[b,c] means a can either be the wire for display b or c
    optionsMap = {}
    for letter in baseMap:
        optionsMap[letter] = baseMap.copy()

    completeInputs = testInputs + numberInputs
    inputsByLength = []
    for i in range(8):
        inputsByLength.append([])
    for testInput in completeInputs:
        inputsByLength[len(testInput)].append(testInput)    
    
    updateoptionsMap(filterMap[1],optionsMap,inputsByLength[2][0])
    updateoptionsMap(filterMap[7],optionsMap,inputsByLength[3][0])
    updateoptionsMap(filterMap[4],optionsMap,inputsByLength[4][0])
    
    # Now that we know some items, elimination becomes a bit easier.
    # There are three numbers with 5 items (2,3 and 5), but we know onthe the 3 contains the 1
    inputs = getInputsContainingLetters(inputsByLength[2][0],inputsByLength[5])
    updateoptionsMap(filterMap[3],optionsMap,inputs[0])

    # To figure out the wires for "c" and "f" we need the 2,5 or 6
    # We can get the 6 by retrieving the opposite of 1
    inputs = getInputsContainingLetters(getOppList(inputsByLength[2][0], baseMap),inputsByLength[6])
    updateoptionsMap(filterMap[6],optionsMap,inputs[0])
    
    #Seems like that does it, all we need to do is translate the number inputs to actual data
    numberString = ''
    for numberInput in numberInputs:
        numberString += inputToNumber(numberInput,optionsMap,filterMap)
    

    return int(numberString)

def inputToNumber(numberInput,optionsMap,filterMap):
    numberOptions = []
    for number,letterMap in enumerate(filterMap):
        if len(letterMap) != len(numberInput):
            continue
        
        if lettersInMap(numberInput,optionsMap,letterMap) == False:
            continue

        return str(number)
    return False

def lettersInMap(numberInput, optionsMap, letterMap):
    for wire in numberInput:
        if optionsMap[wire][0] not in letterMap:
            return False
    return True

def getInputsContainingLetters(letters,inputs):
    for letter in letters:
        inputs = list(filter(lambda wires: letter in wires ,inputs))
    return inputs

def updateoptionsMap(letterMap,optionsMap,lettersString):
    # lettermap defines the shape of the letter
    # optionsmap defines the wires and what part of the letter they might belong to
    # letterString are the wires for which we need to figure out
    # Consider we're dealing with number 1
    # - letterMap would be [c,f]
    # - optionsMap if something like {a:[a,b,c,...],...], we need to remove items from this map based on what we find
    # - letterstip these are the actual wires: e.g "cd"
    #
    # Given the top example, we know that:
    # - wires a,b,e,f,g do not corresond to letter c and f, so we can remove them from the options map
    # - wires c,d do not correspond to letters a,b,d,e,g, so we can remove them

    baseMap = ['a','b','c','d','e','f','g']
    opp = getOppList(letterMap,baseMap)
    for checkLetter in baseMap:
        if checkLetter in lettersString:
            removeOptions(optionsMap,checkLetter,opp)
        else:
            removeOptions(optionsMap,checkLetter,letterMap)

def removeOption(optionsMap,optionLetter,toRemoveLetter):
    if toRemoveLetter in optionsMap[optionLetter]:
        optionsMap[optionLetter].remove(toRemoveLetter)

def removeOptions(optionsMap,optionLetter,toRemoveLetters):
    for toRemoveLetter in toRemoveLetters:
        removeOption(optionsMap,optionLetter,toRemoveLetter)

def getOppList(item,base):
    opp = []
    for checkDigit in base:
        if checkDigit not in item:
            opp.append(checkDigit)
    return opp

def read_file(file):
    file_contents = open("./input/" + file, "r").read().splitlines()
    grouped = []
    for line in file_contents:
        groups  = re.findall('([a-z]+)',line)
        grouped.append([groups[0:10],groups[10:]])
    return grouped
    
part_one('test.txt')
part_one('real.txt')
part_two('test.txt')
part_two('real.txt')
