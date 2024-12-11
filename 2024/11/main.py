import re
import time

def blink(numbers):
    
    newNumbers = {}
    
    for number in numbers:
        createNumbers = []
        count = numbers[number]

        if number == '0':
            createNumbers.append('1')
        elif len(number) % 2 == 0:
            createNumbers.append(number[:int(len(number)/2)])
            createNumbers.append(str(int(number[int(len(number)/2):])))
        else:
            createNumbers.append(str(int(number)*2024))
        
        for newNumber in createNumbers:
            if newNumber not in newNumbers:
                newNumbers[newNumber] = 0
            newNumbers[newNumber] += count
    return newNumbers

def main(filename):
  
    line = open('input/' + filename + '.txt').read().splitlines()[0]
    numbers = re.findall(r'\d+', line)
    numberCounts = {}
    for number in numbers:
        numberCounts[number] = 1

    for i in range(25):
        numberCounts = blink(numberCounts)
    
    total = 0
    for number in numberCounts:
        total += numberCounts[number]
    print('1',filename,total)
    
    total = 0
    for i in range(50):
        numberCounts = blink(numberCounts)
    for number in numberCounts:
        total += numberCounts[number]
    print('2',filename,total)

main('test')
main('real')