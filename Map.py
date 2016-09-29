__author__ = 'lujiji'

from Tkinter import *
import random


width = 160
height = 120
unit = 8
border = 5
highwayLength = 20
allHighways = []

class Location:
    x = 0
    y = 0
    onBoundary = False

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def realX(self):
        if self.x == 0:
            return border
        elif self.x == width-1:
            return width*unit+border
        else:
            return (self.x+0.5)*unit+border

    def realY(self):
        if self.y == 0:
            return border
        elif self.y == height-1:
            return height*unit+border
        else:
            return (self.y+0.5)*unit+border

    def equal(self, loc):
        if self.x == loc.x and self.y == loc.y:
            return True
        else :
            return False


    def checkExceeded(self):
        if self.x >= width-1:
            self.x = width-1
        elif self.y >= height-1:
            self.y = height-1
        elif self.x <= 0:
            self.x = 0
        elif self.y <= 0:
            self.y = 0
        else:
            return False
        self.onBoundary = True
        return True

    def getAllLocations(self, location):
        x1 = min(self.x, location.x)
        x2 = max(self.x, location.x)
        y1 = min(self.y, location.y)
        y2 = max(self.y, location.y)
        allLocations = []
        for i in range(x1,x2+1):
            for j in range(y1, y2+1):
                allLocations.append(Location(i,j))
        return allLocations

    def distance(self, location):
        return abs(self.x-location.x) + abs(self.y-location.y)

def isValidTarget(curLoc, tgLoc):
    locaitons = curLoc.getAllLocations(tgLoc)
    for l in range(0, len(locaitons)):
        loc = locaitons[l]
        if loc.equal(curLoc) is True:
            continue
        if "a" in mapData[loc.y][loc.x] or "b" in mapData[loc.y][loc.x]:
            print(loc.x,loc.y,mapData[loc.y][loc.x])
            return False
    return True

def addHighwayCell(loc):
    status = mapData[loc.y][loc.x]
    if status is "1":
        mapData[loc.y][loc.x] = "a%d" % (len(allHighways))
    elif status is "2":
        mapData[loc.y][loc.x] = "b%d" % (len(allHighways))

def removeHighwayCell(loc):
    status = mapData[loc.y][loc.x]
    if "a" in status:
        mapData[loc.y][loc.x] = "1"
    elif "b" in status:
        mapData[loc.y][loc.x] = "2"

def expandHighway(highway):
    curLoc = highway[-1]
    preLoc = highway[-2]
    locaitons = preLoc.getAllLocations(curLoc)
    if isValidTarget(preLoc, curLoc) is False:
        shrinkHighway(highway)
        return
    for l in range(0, len(locaitons)):
        addHighwayCell(locaitons[l])
    if curLoc.onBoundary is True:
        if len(highway) < 7:
            shrinkHighway(highway)
            return
        else:
            drawHighway(highway)
            return

    i = random.randrange(0, 11)
    nextLoc = Location(0,0)
    if i < 6:
        nextLoc = Location(curLoc.x*2 - preLoc.x, curLoc.y*2 - preLoc.y)
    else:
        power = random.randrange(0,2)
        if curLoc.x == preLoc.x:
            nextLoc = Location(curLoc.x+(-1)**power*highwayLength,curLoc.y)
        else:
            nextLoc = Location(curLoc.x,curLoc.y+(-1)**power*highwayLength)
    nextLoc.checkExceeded()
    highway.append(nextLoc)
    expandHighway(highway)


def shrinkHighway(highway):
    for i in range(0,len(highway)-1):
        curLoc = highway[i]
        nextLoc = highway[i+1]
        locaitons = curLoc.getAllLocations(nextLoc)
        for l in range(0, len(locaitons)):
            removeHighwayCell(locaitons[l])



def drawHighway(highway):
    allHighways.append(highway)
    for i in range(0,len(highway)-1):
        curLoc = highway[i]
        nextLoc = highway[i+1]
        w.create_line(curLoc.realX(),curLoc.realY(),nextLoc.realX(),nextLoc.realY(), fill="blue")


mapData = [["1" for i in range(width)] for j in range(height)]

master = Tk()
w = Canvas(master, width=width*unit+border*2, height=height*unit+border*2)
w.pack()

for i in range(0, width+1):
    w.create_line(unit*i+border, border, unit*i+border, height*unit+border, fill="gray")

for i in range(0, height+1):
    w.create_line(border, unit*i+border, width*unit+border, unit*i+border, fill="gray")

for i in range(0, 8):
    x = random.randrange(15, width-15)
    y = random.randrange(15, height-15)
    for j in range(x-15,x+15):
        for k in range(y-15,y+15):
            if random.randrange(0,2) == 0:
                if mapData[k][j] is not "2":
                    mapData[k][j] = "2"
                    w.create_rectangle(unit*j+border,unit*k+border,unit*(j+1)+border,unit*(k+1)+border, fill="gray")

while len(allHighways)<4:
    highway = []
    x = random.randrange(0, width)
    y = random.randrange(0, height)
    if "a" in mapData[y][x] or "b" in mapData[y][x]:
        continue;
    dir = random.randrange(0,4)
    if dir == 0:
        x = 0
        highway.append(Location(x,y))
        highway.append(Location(x+20,y))
    elif dir == 1:
        y = 0
        highway.append(Location(x,y))
        highway.append(Location(x,y+20))
    elif dir == 2:
        x = width-1
        highway.append(Location(x,y))
        highway.append(Location(x-20,y))
    else:
        y = height-1
        highway.append(Location(x,y))
        highway.append(Location(x,y-20))
    expandHighway(highway)

# Add blocked cells
for i in range(0,int(0.2*width*height)):
    x = random.randrange(0,width)
    y = random.randrange(0,height)
    if random.randrange(0,2) == 0:
        if mapData[y][x] is not "0" and mapData[y][x] is not "2" and "a" not in mapData[y][x] and "b" not in mapData[y][x]:
            mapData[y][x] = "0"
            w.create_rectangle(unit*x+border,unit*y+border,unit*(x+1)+border,unit*(y+1)+border, fill="black")


f = open("./test.txt","w")
for i in range(0,len(mapData)):
    line = ""
    for j in range(0,len(mapData[i])):
        line += "%s," % (mapData[i][j])
    f.write(line[:-2]+"\n")
f.close()


mainloop()
