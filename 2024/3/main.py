import re
from readFile import ReadFile



def main(file):
  total = 0
  lines = ReadFile(file).getLines()
  for line in lines:
    matches = re.findall(r'mul\((\d+), {0,1}(\d+)\)', line)
    for match in matches:
      total += int(match[0]) * int(match[1])

      
  print('Total:', total)


def main2(file):
  total = 0
  lines = ReadFile(file).getLines()
  # line = ''.join(lines)

  lines = [' '.join(lines)]

  for line in lines:

    # line = 'aaadon\'t()bbbbdo()cccccdon\'t()ddddddo()eeee'

    parts = line.split('don\'t()')


    cleanString = parts[0]
    for i in range(1, len(parts)):
      partParts = parts[i].split('do()')
      if(len(partParts) > 1):
        cleanString += ' '.join(partParts[1:])

    # print(cleanString)

    matches = re.findall(r'mul\((\d+),(\d+)\)', cleanString)
    # # print(cleanString)
    # print(matches)
    for match in matches:
      total += int(match[0]) * int(match[1])


    
    # # line = 'aado()aa-vdo()vdon\'t()vv'
    # endsWithDo = re.search(r"do\(\)(?:(?!do\(\)).)(?:(?!don\'t\(\)).)*$", line)
    # if not endsWithDo:
    #   print('No do()')
    # else:
    #   print('Do() found')
    

    # # lastDont = re.findall(r"a-", line)
    # # print('lastDo',lastDo)
    # # print('lastDonr',lastDont)
    # # continue


    rcleanString = re.sub(r'don\'t\(\).*?do\(\)', '', line)
    rcleanString = re.sub(r"don\'t\(\)(?:(?!do\(\)).)(?:(?!don\'t\(\)).)*$", '', rcleanString)
    # print(rcleanString)
    # print(cleanString)
    # # if(re.search(r"don\'t\(\)", cleanString)):
    # #   print('Don\'t found')
    # #   print(cleanString)
    # #   continue

    # # continue

    
  print('Total:', total)
     
main(ReadFile.testFile())
main(ReadFile.realFile())
main2(ReadFile.testFile2())
main2(ReadFile.realFile())