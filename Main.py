__author__ = 'lujiji and SiyuChen'
import Map
from Astar import *
import time

def show(wa, numSG):
    # start = time.clock()
    totalCost = 0
    for j in range(0,numSG):
        startLoc, goalLoc = map.CreateStartGoal() #Map.Location(140,104), Map.Location(1,10)
        print "S-G",j+1
        print "Start point is", mapData[startLoc.y][startLoc.x], startLoc.x, startLoc.y
        print "Goal point is", mapData[goalLoc.y][goalLoc.x], goalLoc.x, goalLoc.y

        path_id, cost = intAstar(startLoc, goalLoc, mapData, wa)
        totalCost += cost
        path_id.append(startLoc)
        path_id.reverse()

        for i in range(0, len(path_id)-1):
            map.DrawLines(path_id[i], path_id[i+1])
    return totalCost/numSG
    # end = time.clock()
    # print 'Running time is:', end-start
    #
    # Map.mainloop()

map = None
path_id = None
cost = 0.0
mapData = None
x = 0
while x != 7:
    display = ["Please input your choice:",
               "1. Create new map",
               "2. Read map from file",
               "3. Execute A* (WA* etc)",
               "4. Save result in file",
               "5. Save map in file",
               "6. Continuous Run",
               "7. Exit",
               "Enter your choice:",
               ]
    x = input("\n".join(display))
    if x == 1:
        map = Map.Map()
        mapData = map.createMap()
    elif x == 2:
        map = Map.Map()
        mapData = map.readMap()
    elif x == 3:
        start = time.clock()
        if map is not None:
            wa = input("input WA:")
            show(wa,1)
            end = time.clock()
            print 'Running time is:', end-start
            Map.mainloop()
    elif x == 4:
        if path_id is not None:
            map.savePath(path_id, cost)
    elif x == 5:
        map.saveMap()
    elif x == 6:
        wa = input("input WA:")
        numMap = 5
        numSG = 10
        pathLength = 0
        start = time.clock()
        for i in range(0,numMap):
            print "map",i+1
            map = Map.Map()
            mapData = map.createMap()
            avgCost = show(wa, numSG)
            pathLength += avgCost
        end = time.clock()
        print 'Running time is:', (end-start)/(numMap*numSG)
        print 'Path length is:', pathLength/numMap
        break
    elif x == 7:
        break
    else:
        print"Wrong number!"
        continue



