import re
import time

def blink(numbers):
    
    new_numbers = {}
    
    for number in numbers:
        count = numbers[number]
        if number == '0':
            if '1' not in new_numbers:
                new_numbers['1'] = count
            else:
                new_numbers['1'] += count
        elif len(number) % 2 == 0:
            first_half = number[:int(len(number)/2)]
            last_half = number[int(len(number)/2):]
            while last_half[0] == '0' and len(last_half) > 1:
                last_half = last_half[1:]

            if first_half not in new_numbers:
                new_numbers[first_half] = count
            else:
                new_numbers[first_half] += count
            if last_half not in new_numbers:
                new_numbers[last_half] = count
            else:
                new_numbers[last_half] += count
        else:
            number = str(int(number)*2024)
            if number not in new_numbers:
                new_numbers[number] = count
            else:
                new_numbers[number] += count
    return new_numbers
    
    # print(numbers)
    # # new_numbers = []
    # # for number in numbers:
    #     if number == '0':
    #         new_numbers.append('1')

    #     elif len(number) % 2 == 0:
    #         new_numbers.append(number[:int(len(number)/2)])
    #         last_half = number[int(len(number)/2):]
    #         while last_half[0] == '0' and len(last_half) > 1:
    #             last_half = last_half[1:]
    #         new_numbers.append(last_half)
    #     # 
    #     else:
    #         new_numbers.append(str(int(number)*2024))
    # return new_numbers

def main(filename):
  
    line = open('input/' + filename + '.txt').read().splitlines()[0]
    numbers = re.findall(r'\d+', line)
    numberCounts = {}
    for number in numbers:
        if number not in numberCounts:
            numberCounts[number] = 1
        else:
            numberCounts[number] += 1

    # new_numbers = []

    for i in range(25):
        numberCounts = blink(numberCounts)
    
    total = 0
    for number in numberCounts:
        total += numberCounts[number]
    print(total)
    
    total = 0
    for i in range(50):
        numberCounts = blink(numberCounts)
    
    for number in numberCounts:
        total += numberCounts[number]
    

    print(total)
main('test')
main('real')