__author__ = 'lujiji and SiyuChen'

from Tkinter import *
import random
import math
from Node import Location
import Astar

class MapLocation(Location):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getAllLocations(self, location):
        x1 = min(self.x, location.x)
        x2 = max(self.x, location.x)
        y1 = min(self.y, location.y)
        y2 = max(self.y, location.y)
        allLocations = []
        for i in range(x1,x2+1):
            for j in range(y1, y2+1):
                allLocations.append(MapLocation(i,j))
        return allLocations

    def distance(self, location):
        return abs(self.x-location.x) + abs(self.y-location.y)

unit = 8.0
border = 5.0
highwayLength = 20

class Map:
    width = 160
    height = 120


    def __init__(self, width = 160, height = 120):
        self.width = width
        self.height = height
        self.mapData = [["1" for i in range(width)] for j in range(height)]
        self.allHighways = []
        self.w = None

    def prepare(self):
        master = Tk()
        frame = Frame(master,width=1200,height=700)
        frame.pack()
        frame.grid(row=0,column=0)
        self.w = Canvas(frame,width=1200,height=700, scrollregion=(0,0,self.width*unit+border*2,self.height*unit+border*2))
        # w = Canvas(master, width=width*unit+border*2, height=height*unit+border*2)
        self.w.bind("<Button-1>", self.callback)
        hbar=Scrollbar(frame,orient=HORIZONTAL)
        hbar.pack(side=BOTTOM,fill=X)
        hbar.config(command=self.w.xview)
        vbar=Scrollbar(frame,orient=VERTICAL)
        vbar.pack(side=RIGHT,fill=Y)
        self.w.config(width=1200,height=650)
        # w.config(width=1290,height=970)
        self.w.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        vbar.config(command=self.w.yview)
        self.w.pack()


    def callback(self, event):
        loc = MapLocation(math.floor((self.w.canvasx(event.x)-border)/unit),math.floor((self.w.canvasy(event.y)-border)/unit))
        Astar.output(loc)
        # print loc.x,loc.y


    def realX(self, loc):
        if loc.x == 0:
            return border
        elif loc.x == self.width-1:
            return self.width*unit+border
        else:
            return (loc.x+0.5)*unit+border
    
    def realY(self, loc):
        if loc.y == 0:
            return border
        elif loc.y == self.height-1:
            return self.height*unit+border
        else:
            return (loc.y+0.5)*unit+border
    
    def checkExceeded(self, loc):
        if loc.x >= self.width-1:
            loc.x = self.width-1
        elif loc.y >= self.height-1:
            loc.y = self.height-1
        elif loc.x <= 0:
            loc.x = 0
        elif loc.y <= 0:
            loc.y = 0
        else:
            return False
        loc.onBoundary = True
        return True
    
    def isValidTarget(self, curLoc, tgLoc):
        locaitons = curLoc.getAllLocations(tgLoc)
        for l in range(0, len(locaitons)):
            loc = locaitons[l]
            if loc == curLoc:
                continue
            if "a" in self.mapData[loc.y][loc.x] or "b" in self.mapData[loc.y][loc.x]:
                return False
        return True
    
    def addHighwayCell(self, loc):
        status = self.mapData[loc.y][loc.x]
        if status is "1":
            self.mapData[loc.y][loc.x] = "a%d" % (len(self.allHighways)+1)
        elif status is "2":
            self.mapData[loc.y][loc.x] = "b%d" % (len(self.allHighways)+1)
    
    def removeHighwayCell(self,loc):
        status = self.mapData[loc.y][loc.x]
        if "a%d" % (len(self.allHighways)+1) in status:
            self.mapData[loc.y][loc.x] = "1"
        elif "b%d" % (len(self.allHighways)+1) in status:
            self.mapData[loc.y][loc.x] = "2"
    
    def expandHighway(self, highway):
        curLoc = highway[-1]
        preLoc = highway[-2]
        locaitons = preLoc.getAllLocations(curLoc)
        if self.isValidTarget(preLoc, curLoc) is False:
            self.shrinkHighway(highway)
            return
        for l in range(0, len(locaitons)):
            self.addHighwayCell(locaitons[l])
        if curLoc.onBoundary is True:
            if len(highway) < 7:
                self.shrinkHighway(highway)
                return
            else:
                self.drawHighway(highway)
                return
    
        i = random.randrange(0, 11)
        nextLoc = MapLocation(0,0)
        if i < 6:
            nextLoc = MapLocation(curLoc.x*2 - preLoc.x, curLoc.y*2 - preLoc.y)
        else:
            power = random.randrange(0,2)
            if curLoc.x == preLoc.x:
                nextLoc = MapLocation(curLoc.x+(-1)**power*highwayLength,curLoc.y)
            else:
                nextLoc = MapLocation(curLoc.x,curLoc.y+(-1)**power*highwayLength)
        self.checkExceeded(nextLoc)
        highway.append(nextLoc)
        self.expandHighway(highway)
    
    
    def shrinkHighway(self,highway):
        for i in range(0,len(highway)-1):
            curLoc = highway[i]
            nextLoc = highway[i+1]
            locaitons = curLoc.getAllLocations(nextLoc)
            for l in range(0, len(locaitons)):
                self.removeHighwayCell(locaitons[l])
    
    
    
    def drawHighway(self, highway):
        self.allHighways.append(highway)
        for i in range(0,len(highway)-1):
            curLoc = highway[i]
            nextLoc = highway[i+1]
            self.w.create_line(self.realX(curLoc),self.realY(curLoc),self.realX(nextLoc),self.realY(nextLoc), fill="blue")
    
    def createGrid(self):
        for i in range(0, self.width+1):
            self.w.create_line(unit*i+border, border, unit*i+border, self.height*unit+border, fill="gray")
        for i in range(0, self.height+1):
            self.w.create_line(border, unit*i+border, self.width*unit+border, unit*i+border, fill="gray")
    
    def createMap(self):
        self.prepare()
        self.createGrid()
        for i in range(0, 8):
            x = random.randrange(15, self.width-15)
            y = random.randrange(15, self.height-15)
            for j in range(x-15,x+15):
                for k in range(y-15,y+15):
                    if random.randrange(0,2) == 0:
                        if self.mapData[k][j] is not "2":
                            self.mapData[k][j] = "2"
                            self.w.create_rectangle(unit*j+border,unit*k+border,unit*(j+1)+border,unit*(k+1)+border, fill="gray")
    
        while len(self.allHighways)<4:
            highway = []
            x = random.randrange(0, self.width)
            y = random.randrange(0, self.height)
            if "a" in self.mapData[y][x] or "b" in self.mapData[y][x]:
                continue;
            dir = random.randrange(0,4)
            if dir == 0:
                x = 0
                highway.append(MapLocation(x,y))
                highway.append(MapLocation(x+20,y))
            elif dir == 1:
                y = 0
                highway.append(MapLocation(x,y))
                highway.append(MapLocation(x,y+20))
            elif dir == 2:
                x = self.width-1
                highway.append(MapLocation(x,y))
                highway.append(MapLocation(x-20,y))
            else:
                y = self.height-1
                highway.append(MapLocation(x,y))
                highway.append(MapLocation(x,y-20))
            self.expandHighway(highway)
    
        # Add blocked cells
        num_blocked = 0
        while num_blocked < int(0.2*self.width*self.height):
            x = random.randrange(0, self.width)
            y = random.randrange(0, self.height)
            if self.mapData[y][x] not in ["0", "2"] and "a" not in self.mapData[y][x] and "b" not in self.mapData[y][x]:
                self.mapData[y][x] = "0"
                self.w.create_rectangle(unit*x+border, unit*y+border, unit*(x+1)+border, unit*(y+1)+border, fill="black")
                num_blocked += 1
        return self.mapData
    
    def GenerateStartGoal(self):
        possibility= random.randrange(0, 2)
        position_x = possibility*random.randrange(0, 20)+ (1-possibility)*random.randrange(self.width-20, self.width)
        position_y = possibility*random.randrange(0, 20)+ (1-possibility)*random.randrange(self.height-20, self.height)
        return position_x, position_y
    
    def CreateStartGoal(self):
    
        start_x, start_y = self.GenerateStartGoal()
        while self.mapData[start_y][start_x] == "0":
            start_x, start_y = self.GenerateStartGoal()
    
        goal_x, goal_y = self.GenerateStartGoal()
        while self.mapData[goal_y][goal_x] == "0":
            goal_x, goal_y = self.GenerateStartGoal()
    
        while math.sqrt((start_x - goal_x)**2+(start_y - goal_y)**2) < 100:
            start_x, start_y = self.GenerateStartGoal()
            while self.mapData[start_y][start_x] == "0":
                start_x, start_y = self.GenerateStartGoal()
            while self.mapData[goal_y][goal_x] == "0":
                goal_x, goal_y = self.GenerateStartGoal()
        self.w.create_oval(unit*start_x+border+1, unit*start_y+border+1, unit*(start_x+1)+border-1, unit*(start_y+1)+border-1, fill="red")
        self.w.create_oval(unit*goal_x+border+1, unit*goal_y+border+1, unit*(goal_x+1)+border-1, unit*(goal_y+1)+border-1, fill="green")
        return MapLocation(start_x,start_y),MapLocation(goal_x,goal_y)
    
    def DrawLines(self,locstart, locend):
        self.w.create_line((locstart.x+0.5)*unit+border, (locstart.y+0.5)*unit+border, (locend.x+0.5)*unit+border,(locend.y+0.5)*unit+border, fill="red", width= 3)
    
    def savePath(self,path_id, cost):
        f = open("./path.txt","w")
        f.write("%f" % (cost))
        for i in range(0,len(path_id)):
            line = "%s,%s" % (path_id[i].x, path_id[i].y)
            f.write("\n"+line[:-1])
        f.close()
    
    def saveMap(self):
        f = open("./test.txt","w")
        f.write("%d,%d" % (self.height,self.width))
        for i in range(0,len(self.mapData)):
            line = ""
            for j in range(0,len(self.mapData[i])):
                line += "%s," % (self.mapData[i][j])
            f.write("\n"+line[:-1])
        f.close()
    
    def readMap(self):
        content = open("./test.txt").read()
        lines = content.split("\n")
        self.mapData = []
        self.width = int(lines[0].split(",")[1])
        self.height = int(lines[0].split(",")[0])
        self.prepare()
        for i in range(1, len(lines)):
            self.mapData.append(lines[i].split(","))
            # print(id(mapData))
    
        self.createGrid()
        for y in range(0,len(self.mapData)):
            for x in range(0,len(self.mapData[y])):
                status = self.mapData[y][x]
                if status is "0":
                    self.w.create_rectangle(x*unit+border,y*unit+border,(x+1)*unit+border,(y+1)*unit+border, fill="black")
                elif status is "2" or "b" in status:
                    self.w.create_rectangle(x*unit+border,y*unit+border,(x+1)*unit+border,(y+1)*unit+border, fill="gray")
        for y in range(0,len(self.mapData)):
            for x in range(0,len(self.mapData[y])):
                status = self.mapData[y][x]
                if "b" in status or "a" in status:
                    curLoc = MapLocation(x,y)
                    nextLoc = None
                    if x+1<len(self.mapData[y]) and len(self.mapData[y][x+1]) == 2 and status[-1] == self.mapData[y][x+1][-1]:
                        nextLoc = MapLocation(x+1,y)
                        self.w.create_line(self.realX(curLoc),self.realY(curLoc),self.realX(nextLoc),self.realY(nextLoc), fill="blue")
                    if y+1<len(self.mapData) and len(self.mapData[y+1][x]) == 2 and status[-1] == self.mapData[y+1][x][-1]:
                        nextLoc = MapLocation(x,y+1)
                        self.w.create_line(self.realX(curLoc),self.realY(curLoc),self.realX(nextLoc),self.realY(nextLoc), fill="blue")
        return self.mapData
