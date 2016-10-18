__author__ = 'lujiji and SiyuChen'
import Map
from Astar import *
import time

def show(w1, w2, numSG, read = False):
    # start = time.clock()
    totalCostSeq = 0
    totalCostInt = 0
    totalNodeSeq = 0
    totalNodeInt = 0
    for j in range(0,numSG):
        startLoc = None
        goalLoc = None
        if read is True:
            startLoc = map.start
            goalLoc = map.goal
        else:
            startLoc, goalLoc = map.CreateStartGoal()
        # startLoc, goalLoc = map.CreateStartGoal() #Map.Location(140,104), Map.Location(1,10)
        print "S-G",j+1
        print "Start point is", mapData[startLoc.y][startLoc.x], startLoc.x, startLoc.y
        print "Goal point is", mapData[goalLoc.y][goalLoc.x], goalLoc.x, goalLoc.y

        map.algorithm = AstarSeq(mapData, w1, w2)
        path_id, costSeq, numNodesSeq = map.algorithm.execute(startLoc, goalLoc)
        map.algorithm = AstarInt(mapData, w1, w2)
        path_id, costInt, numNodesInt = map.algorithm.execute(startLoc, goalLoc)

        # path_id, cost, numNodes = intAstar(startLoc, goalLoc, mapData, wa)
        print "Memory cost %.2f" % (map.algorithm.maxMemory)
        totalCostSeq += costSeq
        totalCostInt += costInt
        totalNodeSeq += numNodesSeq
        totalNodeInt += numNodesInt
        path_id.append(startLoc)
        path_id.reverse()

        for i in range(0, len(path_id)-1):
            map.DrawLines(path_id[i], path_id[i+1])
    return totalCostSeq/numSG, totalNodeSeq/numSG, totalCostInt/numSG, totalNodeInt/numSG
    # end = time.clock()
    # print 'Running time is:', end-start
    #
    # Map.mainloop()

map = None
path_id = None
cost = 0.0
mapData = None
x = 0
read = False
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
        read = False
    elif x == 2:
        map = Map.Map()
        mapData = map.readMap()
        read = True
    elif x == 3:
        start = time.clock()
        if map is not None:
            w1 = input("input W1:")
            w2 = input("input W2:")
            show(w1,w2, 1, read)

            end = time.clock()
            print 'Running time is:', end-start
            Map.mainloop()
    elif x == 4:
        if path_id is not None:
            map.savePath(path_id, cost)
    elif x == 5:
        map.saveMap()
    elif x == 6:
        w1 = input("input W1:")
        w2 = input("input W2:")
        numMap = 5
        numSG = 10
        pathLengthSeq = 0
        nodeExpandSeq = 0
        pathLengthInt = 0
        nodeExpandInt = 0
        start = time.clock()
        for i in range(0,numMap):
            print "map",i+1
            map = Map.Map()
            mapData = map.createMap()
            avgCostSeq, avgNodeSeq, avgCostInt, avgNodeInt = show(w1, w2, numSG)
            pathLengthSeq += avgCostSeq
            nodeExpandSeq += avgNodeSeq
            pathLengthInt += avgCostInt
            nodeExpandInt += avgNodeInt
        end = time.clock()

        print "Sequential:"
        # print 'Running time is:', (end-start)/(numMap*numSG)
        print 'Path length is:', pathLengthSeq/numMap
        print 'Number of nodes expanded is:', nodeExpandSeq/numMap

        print "Integrated:"
        # print 'Running time is:', (end-start)/(numMap*numSG)
        print 'Path length is:', pathLengthInt/numMap
        print 'Number of nodes expanded is:', nodeExpandInt/numMap
        break
    elif x == 7:
        break
    else:
        print"Wrong number!"
        continue



