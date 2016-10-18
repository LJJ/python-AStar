__author__ = 'lujiji and SiyuChen'
import Map
from Astar import *
import time

def show(w1, w2, numSG, read = False):
    # start = time.clock()
    totalCostSeq = 0
    totalCostInt = 0
    totalCostOrig = 0
    totalNodeSeq = 0
    totalNodeInt = 0
    totalNodeOrig = 0
    memorySeq = 0.0
    memoryInt = 0.0
    memoryOrig = 0.0
    durationOrig = 0.0
    durationSeq = 0.0
    durationInt = 0.0
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

        # algorithms = [Astar(mapData, w1, w2),AstarSeq(mapData, w1, w2),AstarInt(mapData, w1, w2)]
        #
        # for i in range(len(algorithms)):
        #     map.algorithm = algorithms[i]

        clock1 = time.clock()
        map.algorithm = Astar(mapData, w1, w2)
        result = map.algorithm.execute(startLoc, goalLoc)
        durationOrig += time.clock() - clock1
        memoryOrig += map.algorithm.maxMemory
        totalCostOrig += result[1]
        totalNodeOrig += result[2]



        clock1 = time.clock()

        map.algorithm = AstarSeq(mapData, w1, w2)
        result = map.algorithm.execute(startLoc, goalLoc)
        durationSeq += time.clock() - clock1
        memorySeq += map.algorithm.maxMemory
        totalCostSeq += result[1]
        totalNodeSeq += result[2]

        clock1 = time.clock()
        map.algorithm = AstarInt(mapData, w1, w2)
        result = map.algorithm.execute(startLoc, goalLoc)
        durationInt += time.clock() - clock1
        memoryInt += map.algorithm.maxMemory
        totalCostInt += result[1]
        totalNodeInt += result[2]

        # path_id, cost, numNodes = intAstar(startLoc, goalLoc, mapData, wa)

        # path_id.append(startLoc)
        # path_id.reverse()
        #
        # for i in range(0, len(path_id)-1):
        #     map.DrawLines(path_id[i], path_id[i+1])
    return totalCostOrig/numSG, totalNodeOrig/numSG, memoryOrig/numSG, durationOrig/numSG, totalCostSeq/numSG, totalNodeSeq/numSG, memorySeq/numSG,durationSeq/numSG, totalCostInt/numSG, totalNodeInt/numSG, memoryInt/numSG, durationInt/numSG
    # end = time.clock()
    # print 'Running time is:', end-start
    #
    # Map.mainloop()


def showSingle(w1, w2, read = False):
    if read is False:
        startLoc, goalLoc = map.CreateStartGoal()
    else:
        startLoc = map.start
        goalLoc = map.goal

    map.algorithm = Astar(mapData, w1, w2)
    path_id, cost, nodes  = map.algorithm.execute(startLoc, goalLoc)

    path_id.append(startLoc)
    path_id.reverse()
    for i in range(0, len(path_id)-1):
        map.DrawLines(path_id[i], path_id[i+1])

    return cost, 0


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
            avgCost, avgNode = showSingle(w1,w2, read)
            print 'cost:', avgCost
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
        numMap = 3
        numSG = 5
        pathLengthSeq = 0
        nodeExpandSeq = 0
        pathLengthInt = 0
        nodeExpandInt = 0
        memorySeq = 0.0
        memoryInt = 0.0
        pathLengthOrig = 0.0
        nodeExpandOrig = 0
        memoryOrig = 0.0
        durOrig = 0.0
        durInt = 0.0
        durSeq = 0.0
        start = time.clock()
        for i in range(0,numMap):
            print "map",i+1
            map = Map.Map()
            mapData = map.createMap()
            avgCostOrig, avgNodeOrig, avgMemoryOrig,avgDurOrig, avgCostSeq, avgNodeSeq, avgMemorySeq,avgDurSeq, avgCostInt, avgNodeInt, avgMemoryInt,avgDurInt = show(w1, w2, numSG)
            pathLengthSeq += avgCostSeq
            nodeExpandSeq += avgNodeSeq
            pathLengthInt += avgCostInt
            nodeExpandInt += avgNodeInt
            memoryInt +=avgMemoryInt
            memorySeq += avgMemorySeq
            nodeExpandOrig += avgNodeOrig
            pathLengthOrig += avgCostOrig
            memoryOrig += avgMemoryOrig
            durOrig += avgDurOrig
            durInt += avgDurInt
            durSeq += avgDurSeq
        end = time.clock()

        print "Original:"
        # print 'Running time is:', (end-start)/(numMap*numSG)
        print 'Path length is:', pathLengthOrig/numMap
        print 'Time:', durOrig/numMap
        print 'Number of nodes expanded is:', nodeExpandOrig/numMap ,"   Memory:", avgMemoryOrig/numMap

        print "Sequential:"
        # print 'Running time is:', (end-start)/(numMap*numSG)
        print 'Path length is:', pathLengthSeq/numMap
        print 'Time:', durSeq/numMap
        print 'Number of nodes expanded is:', nodeExpandSeq/numMap , "   Memory:", avgMemorySeq/numMap

        print "Integrated:"
        print 'Path length is:', pathLengthInt/numMap
        print 'Time:', durInt/numMap
        print 'Number of nodes expanded is:', nodeExpandInt/numMap ,"   Memory:", avgMemoryInt/numMap
        break
    elif x == 7:
        break
    else:
        print"Wrong number!"
        continue



