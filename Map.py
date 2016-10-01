__author__ = 'lujiji and SiyuChen'

from Tkinter import *
import random
import math
width = 160
height = 120
mapData = [["1" for i in range(width)] for j in range(height)]
print(id(mapData))
unit = 8
border = 5
highwayLength = 20
allHighways = []

master = Tk()
frame = Frame(master,width=1200,height=700)
frame.grid(row=0,column=0)
w = Canvas(frame,width=1200,height=700, scrollregion=(0,0,width*unit+border*2,height*unit+border*2))
# w = Canvas(master, width=width*unit+border*2, height=height*unit+border*2)
hbar=Scrollbar(frame,orient=HORIZONTAL)
hbar.pack(side=BOTTOM,fill=X)
hbar.config(command=w.xview)
vbar=Scrollbar(frame,orient=VERTICAL)
vbar.pack(side=RIGHT,fill=Y)
w.config(width=1200,height=650)
# w.config(width=1290,height=970)
w.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
vbar.config(command=w.yview)
w.pack()

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
            return False
    return True

def addHighwayCell(loc):
    status = mapData[loc.y][loc.x]
    if status is "1":
        mapData[loc.y][loc.x] = "a%d" % (len(allHighways)+1)
    elif status is "2":
        mapData[loc.y][loc.x] = "b%d" % (len(allHighways)+1)

def removeHighwayCell(loc):
    status = mapData[loc.y][loc.x]
    if "a%d" % (len(allHighways)+1) in status:
        mapData[loc.y][loc.x] = "1"
    elif "b%d" % (len(allHighways)+1) in status:
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

def createGrid():
    for i in range(0, width+1):
        w.create_line(unit*i+border, border, unit*i+border, height*unit+border, fill="gray")
    for i in range(0, height+1):
        w.create_line(border, unit*i+border, width*unit+border, unit*i+border, fill="gray")

def createMap():
    createGrid()
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
    num_blocked = 0
    while num_blocked < int(0.2*width*height):
        x = random.randrange(0, width)
        y = random.randrange(0, height)
        if mapData[y][x] not in ["0", "2"] and "a" not in mapData[y][x] and "b" not in mapData[y][x]:
            mapData[y][x] = "0"
            w.create_rectangle(unit*x+border, unit*y+border, unit*(x+1)+border, unit*(y+1)+border, fill="black")
            num_blocked += 1
    saveMap()

def GenerateStartGoal():
    possibility= random.randrange(0, 2)
    position_x = possibility*random.randrange(0, 20)+ (1-possibility)*random.randrange(width-20, width)
    position_y = possibility*random.randrange(0, 20)+ (1-possibility)*random.randrange(height-20, height)
    return position_x, position_y

def CreateStartGoal():
    start_x, start_y = GenerateStartGoal()
    while mapData[start_y][start_x] is "0":
        start_x, start_y = GenerateStartGoal()

    goal_x, goal_y = GenerateStartGoal()
    while mapData[goal_y][goal_x] is "0":
        goal_x, goal_y = GenerateStartGoal()

    while math.sqrt((start_x - goal_x)**2+(start_y - goal_y)**2) < 100:
        start_x, start_y = GenerateStartGoal()
        while mapData[start_y][start_x] is "0":
            start_x, start_y = GenerateStartGoal()
            goal_x, goal_y = GenerateStartGoal()
        while mapData[goal_y][goal_x] is "0":
            goal_x, goal_y = GenerateStartGoal()
    w.create_oval(unit*start_x+border+1, unit*start_y+border+1, unit*(start_x+1)+border-1, unit*(start_y+1)+border-1, fill="red")
    w.create_oval(unit*goal_x+border+1, unit*goal_y+border+1, unit*(goal_x+1)+border-1, unit*(goal_y+1)+border-1, fill="green")
    return start_x, start_y, goal_x, goal_y

def DrawLines(locstart, locend):
    w.create_line((locstart[0]+0.5)*unit+border, (locstart[1]+0.5)*unit+border, (locend[0]+0.5)*unit+border,(locend[1]+0.5)*unit+border, fill="red", width= 3)

def savePath(path_id, cost):
    f = open("./path.txt","w")
    f.write("%f" % (cost))
    for i in range(0,len(path_id)):
        line = ""
        for j in range(0,len(path_id[i])):
            line += "%s," % (path_id[i][j])
        f.write("\n"+line[:-1])
    f.close()

def saveMap():
    f = open("./test.txt","w")
    f.write("%d,%d" % (height,width))
    for i in range(0,len(mapData)):
        line = ""
        for j in range(0,len(mapData[i])):
            line += "%s," % (mapData[i][j])
        f.write("\n"+line[:-1])
    f.close()

def readMap():
    content = open("./test.txt").read()
    lines = content.split("\n")
    mapData = []
    width = int(lines[0].split(",")[1])
    height = int(lines[0].split(",")[0])
    for i in range(1, len(lines)):
        mapData.append(lines[i].split(","))

    createGrid()
    for y in range(0,len(mapData)):
        for x in range(0,len(mapData[y])):
            status = mapData[y][x]
            if status is "0":
                w.create_rectangle(x*unit+border,y*unit+border,(x+1)*unit+border,(y+1)*unit+border, fill="black")
            elif status is "2" or "b" in status:
                w.create_rectangle(x*unit+border,y*unit+border,(x+1)*unit+border,(y+1)*unit+border, fill="gray")
    for y in range(0,len(mapData)):
        for x in range(0,len(mapData[y])):
            status = mapData[y][x]
            if "b" in status or "a" in status:
                curLoc = Location(x,y)
                nextLoc = None
                print(x,y)
                if x+1<len(mapData[y]) and len(mapData[y][x+1]) == 2 and status[-1] == mapData[y][x+1][-1]:
                    nextLoc = Location(x+1,y)
                    w.create_line(curLoc.realX(),curLoc.realY(),nextLoc.realX(),nextLoc.realY(), fill="blue")
                if y+1<len(mapData) and len(mapData[y+1][x]) == 2 and status[-1] == mapData[y+1][x][-1]:
                    nextLoc = Location(x,y+1)
                    w.create_line(curLoc.realX(),curLoc.realY(),nextLoc.realX(),nextLoc.realY(), fill="blue")
    #mainloop()
#mainloop()
