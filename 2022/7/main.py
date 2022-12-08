from enum import unique
import re
import statistics

def part_one(file):
    currentDir = read_file(file)
    
    dirs = filter(lambda size: size <= 100000,currentDir.listSizes())
    print(sum(dirs))
    
def part_two(file):
    currentDir = read_file(file)
    
    diskSize = 70000000
    needed = 30000000
    freeSpace = diskSize - currentDir.getSize()
    toFree = needed-freeSpace
    dirs = list(filter(lambda size: size >= toFree,currentDir.listSizes()))
    dirs.sort()
    print(dirs)
    print(dirs[0])
    
def read_file(file):
    lines = open("./input/" + file, "r").read().splitlines()

    currentCommand=False
    currentDir= Folder('/')

    for line in lines[1:]:
        lineParts = line.split(' ')
        if lineParts[0] == '$':
            currentCommand = False
            if lineParts[1] == 'ls':
                currentCommand = 'list'
            elif lineParts[1] == 'cd':
                currentDir.changeDir(lineParts[2])
            else:
                print('unknown command', lineParts[1])
        else:
            if(currentCommand == 'list'):
                currentDir.addContent(lineParts[0],lineParts[1])    
    return currentDir


class File:
    def __init__(self,name,size) -> None:
        self.name = name
        self.size = size
        pass

class Folder:
    def __init__(self,name) -> None:
        self.name = name
        self.folders = []
        self.files = []
        self.currentFolder = False
        pass
    def addContent(self,type,name):
        if self.currentFolder:
            self.currentFolder.addContent(type,name)
        else:
            if type == 'dir':
                self.folders.append(Folder(name))
            else:
                self.files.append(File(name,int(type)))
    def changeDir(self,part):
        if part == '..':
            if self.currentFolder:
                if self.currentFolder.currentFolder:
                    self.currentFolder.changeDir(part)
                else:
                    self.currentFolder = False
            else:
                print('ERROR: already in root')
        else:
            if self.currentFolder:
                self.currentFolder.changeDir(part)
            else:
                for f in self.folders:
                    if f.name == part:
                        self.currentFolder = f
                        break

    def getSize(self):
        size = 0
        for d in self.folders:
            size += d.getSize()
        for f in self.files:
            size+=f.size
        return(size)
    
    def listSizes(self):
        sizes = [self.getSize()]
        for d in self.folders:
            sizes += d.listSizes()
        return sizes
         
part_one('test.txt')
part_one('real.txt')
part_two('test.txt')
part_two('real.txt')
