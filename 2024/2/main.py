import re
from readFile import ReadFile


def arrayDiff(arr):
  diff = []
  for i in range(len(arr) - 1):
    diff.append(arr[i+1] - arr[i])
  return diff

def lineOk(line):
  lineDiff = arrayDiff(line)
  count = sum(1 for i in lineDiff if i < -3 or i > 3 or i == 0)
  if(count > 0):
    return False
  
  count = 0
  for i in range(len(lineDiff)):
    count += 1 if lineDiff[i] > 0  else -1
  return len(lineDiff) == abs(count)

def main(file):
  total = 0
  lines = ReadFile(file).splitLinesInt()
  for line in lines:   
    if(lineOk(line)):
      total += 1
  print('Total:', total)

def cutLine(line):
  lines = []
  for i in range(len(line)):
    cutLine = line.copy()
    cutLine.pop(i)
    lines.append(cutLine)
    
  return lines

def main2(file):
  total = 0
  lines = ReadFile(file).splitLinesInt()
  for line in lines:
    if(lineOk(line)):
      total += 1
      continue

    for cut in cutLine(line):
      if(lineOk(cut)):
        total += 1
        break


  print('Total:', total)
     
main(ReadFile.testFile())
main(ReadFile.realFile())
main2(ReadFile.testFile())
main2(ReadFile.realFile())






