import re
from readFile import ReadFile


def parseFile(file):
  file = ReadFile(file)
  lines = file.getLines()

  pairs = [[],[]]
  for line in lines:
    # Match all numbers
    numbers = list(map(int, re.findall(r'\d+', line)))
    pairs[0].append(numbers[0])
    pairs[1].append(numbers[1])

  return pairs

def main(file):

  pairs = parseFile(file)

  # Sort the pairs
  pairs[0].sort()
  pairs[1].sort()

  total = 0
  for i in range(len(pairs[0])):
    diff = abs(pairs[0][i] - pairs[1][i])
    total += diff
  
  print('Total:', total)

def main2(file):
  pairs = parseFile(file)
  total = 0
  for i in range(len(pairs[0])):
    num1 = pairs[0][i]
    total += pairs[1].count(num1) * num1
  print('Total:', total)
    
main(ReadFile.testFile())
main(ReadFile.realFile())
main2(ReadFile.testFile())
main2(ReadFile.realFile())






