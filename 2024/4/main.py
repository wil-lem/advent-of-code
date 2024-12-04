import re
from readFile import ReadFile

def getWord(x,y,dx,dy,lines,maxLength=4):
  word = ''
  while(x >= 0 and y >= 0 and x < len(lines) and y < len(lines[x]) and len(word) < maxLength):
    word += lines[x][y]
    x += dx
    y += dy
  return word


def countMasX(x,y,lines):
  words= [
    getWord(x-1,y-1,1,1,lines,3),
    getWord(x-1,y+1,1,-1,lines,3)
  ]
  return (len([word for word in words if 'MAS' == word or 'SAM' == word])) == 2

def countXmas(x,y,lines):
  words = []
  for dx in range(-1,2):
    for dy in range(-1,2):
      words.append(getWord(x,y,dx,dy,lines))
  countXmas = len([word for word in words if 'XMAS' in word])
  return countXmas

def main(file):
  lines = ReadFile(file).getLines()
  total = 0
  for x in range(len(lines)):
    for y in range(len(lines[x])):
      total  += countXmas(x,y,lines)
  
  print('Total:', total)


def main2(file):
  lines = ReadFile(file).getLines()
  line = ''.join(lines)


  total = 0
  for x in range(len(lines)):
    for y in range(len(lines[x])):
      total  += 1 if countMasX(x,y,lines) else 0
  

  print('Total:', total)
     
main(ReadFile.testFile())
main(ReadFile.realFile())
main2(ReadFile.testFile())
main2(ReadFile.realFile())