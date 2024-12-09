import re
import time
from readFile import ReadFile


def parseFile(filename):
    rf = ReadFile(filename)
    lines = rf.getLines()
    
    isFile = True
    files = []
    spaces = []
    id = 0
    index = 0

    for char in lines[0]:
        size = int(char)
        if isFile:
            files.append({'size':size,'id':id,'index':index})
            id += 1
        else:
            spaces.append({'size':size,'index':index})
        isFile = not isFile
        index += size

    return files, spaces
    
def main(filename):
    files, spaces = parseFile(filename)
    
    mod = 0
    total = 0
    checkline = ''
    for i,f in enumerate(files):
        file = files[i]
        size = file['size']
        id = file['id']

        for j in range(size):
            file['size'] -= 1
            total += file['id'] * mod
            mod += 1
            checkline += str(id)

        space = spaces[i]

        for j in range(space['size']):
            
            lastFile = files[-1:][0]
            size = lastFile['size']
            if size == 0:
                files.pop()
                continue
            total += lastFile['id'] * mod
            mod += 1
            checkline += str(lastFile['id'])
            
            lastFile['size'] -= 1
            if lastFile['size'] == 0:
                files.pop()

    print(total)

def main2(filename):

    startTime = time.time()

    files, spaces = parseFile(filename)

    total = 0

    for file in reversed(files):
        size = file['size']
        index = file['index']
        for i,space in enumerate(spaces):

            spaceSize = space['size']

            if space['size'] >= size and space['index'] < index:
                space[1] = index
                file['index'] = space['index']

                if spaceSize == size:
                    spaces.pop(i)
                else:
                    space['size'] -= size
                    space['index'] += size
                
                break
        for i in range(file['size']):
            total += file['id'] * (i+file['index'])

    # sortedFiles = sorted(files, key=lambda x: x['index'])
    print(total)
    print('Time:',time.time()-startTime)
    
main(ReadFile.testFile())
main(ReadFile.realFile())
main2(ReadFile.testFile())
main2(ReadFile.realFile())