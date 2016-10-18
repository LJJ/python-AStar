__author__ = 'SiyuChen and lujiji'
from math import *
import BinaryHeap
import Node
from Heuristic import *


fringeArray = []#BinaryHeap.BinaryHeap()
closedArray = []
mapData = None
parentArray = []
fValueArray = []
gValueArray = []
exist = {}
result_i = 0
heuristicArray = [HeuristicOptimal,HeuristicOne,HeuristicTwo,HeuristicThree,HeuristicFour]

def resetAllData(amount):
    global fringeArray
    fringeArray = [BinaryHeap.BinaryHeap() for i in range(amount)]
    global closedArray
    closedArray = [{} for i in range(amount)]
    global parentArray
    parentArray = [{} for i in range(amount)]
    global gValueArray
    gValueArray = [{} for i in range(amount)]
    global hValueArray
    hValueArray = [{} for i in range(amount)]
    global fValueArray
    fValueArray = [{} for i in range(amount)]
    global exist
    exist = {}

def Astar(sStart, sGoal, mapD, wa):
    # A-star algorithm
    resetAllData(1)
    global mapData
    mapData = mapD

    cost = 0.0
    gValue = gValueArray[0]
    parent = parentArray[0]
    fringe = fringeArray[0]
    closed = closedArray[0]

    w=wa
    gValue[sStart.key()] = 0.0
    fringe.insert(sStart, HeuristicOptimal.hValue(sStart, sGoal))
    path_id = []

    while fringe.count() > 0:
        s = fringe.pop()
        if s == sGoal:
            print "path found"
            cost = s.fValue
            print "cost: %f" % (cost)
            loc1 = findPath(s,0)
            break
        closed[s.key()] = s
        expand(s,sGoal,0)
    return path_id, cost


def seqAstar(sStart, sGoal, mapD, wa):
    # A-star algorithm
    resetAllData(len(heuristicArray))
    global mapData
    mapData = mapD
    w1 = 1.0
    w2 = 1.0
    for i in range(0,len(heuristicArray)):
        gValueArray[i][sStart.key()] = 0.0
        gValueArray[i][sGoal.key()] = float('inf')
        fringeArray[i].insert(sStart,w1*heuristicArray[i].hValue(sStart,sGoal))

    while fringeArray[0].minValue() < float('inf'):
        for i in range(1, len(heuristicArray)):
            if fringeArray[i].minValue() <= w2*fringeArray[0].minValue():
                if gValueArray[i][sGoal.key()] < fringeArray[i].minValue():
                    if gValueArray[i][sGoal.key()] < float('inf'):
                        path_id = findPath(sGoal, i)
                        global result_i
                        result_i = i
                        return path_id, fringeArray[i].getFvalue(sGoal)
                else:
                    s = fringeArray[i].pop()
                    expand(s,sGoal,i)
            else:
                if gValueArray[0][sGoal.key()] <= fringeArray[0].minValue():
                    if gValueArray[0][sGoal.key()] < float('inf'):
                        path_id =findPath(sGoal, 0)
                        global result_i
                        result_i = 0
                        return path_id, fringeArray[0].getFvalue(sGoal)
                else:
                    s = fringeArray[0].pop()
                    expand(s,sGoal,0)
    return [], fringeArray[0].getFvalue(sGoal)

def expand(s, goal, i):
    w1 = 1.0
    gValue = gValueArray[i]
    parent = parentArray[i]
    fringe = fringeArray[i]
    closed = closedArray[i]
    previousMinValue = 0
    closed[s.key()] = s
    for m in range(-1,2):
            for n in range(-1,2):
                if not(m == 0 and n == 0):
                    if s.y+n > 119 or s.x+m > 159 or s.y+n < 0 or s.x+m < 0:
                        continue
                    if mapData[s.y+n][s.x+m] is not "0":
                        s_prime = Node.Location(s.x+m, s.y+n)
                        if closed.has_key(s_prime.key()) is False:
                            temp_gValue = gValue[s.key()] + distance(s, s_prime)
                            if fringe.has(s_prime) is False:
                                gValue[s_prime.key()] = float('inf') #warning
                                status = True
                            else:
                                # s_prime = fringe.getLoc(s_prime.key())  #don't remove
                                if temp_gValue < gValue[s_prime.key()]:
                                    status = True
                                else:
                                    status = False
                            if status == True:
                                parent[s_prime.key()] = s
                                gValue[s_prime.key()] = temp_gValue
                                fringe.insert(s_prime, gValue[s_prime.key()]+w1*heuristicArray[i].hValue(s_prime,goal))

def intAstar(sStart, sGoal, mapD, wa):
    resetAllData(len(heuristicArray))
    global mapData
    mapData = mapD
    w1 = 1.0
    w2 = 1.0
    gValueArray[0][sStart.key()] = 0.0
    gValueArray[0][sGoal.key()] = float('inf')
    exist[sStart.key()] = True
    for i in range(0,len(heuristicArray)):
        fringeArray[i].insert(sStart,w1*heuristicArray[i].hValue(sStart,sGoal))

    while fringeArray[0].minValue() < float('inf'):
        for i in range(1, len(heuristicArray)):
            if fringeArray[i].minValue() <= w2*fringeArray[0].minValue():
                if gValueArray[0][sGoal.key()] < fringeArray[i].minValue():
                    if gValueArray[0][sGoal.key()] < float('inf'):
                        path_id = findPath(sGoal, 0)
                        return path_id, fringeArray[0].getFvalue(sGoal)
                else:
                    s = fringeArray[i].pop()
                    expandInt(s,sGoal)
                    closedArray[1][s.key()] = s
            else:
                if gValueArray[0][sGoal.key()] <= fringeArray[0].minValue():
                    if gValueArray[0][sGoal.key()] < float('inf'):
                        path_id =findPath(sGoal, 0)
                        return path_id, fringeArray[0].getFvalue(sGoal)
                else:
                    s = fringeArray[0].pop()
                    expandInt(s,sGoal)
                    closedArray[0][s.key()] = s
    return [], fringeArray[0].getFvalue(sGoal)

def expandInt(s, goal):
    w1 = 1.0
    gValue = gValueArray[0]
    for i in range(len(fringeArray)):
        fringeArray[i].remove(s)

    parent = parentArray[0]
    # closed = closedArray[i]
    for m in range(-1,2):
            for n in range(-1,2):
                if not(m == 0 and n == 0):
                    if s.y+n > 119 or s.x+m > 159 or s.y+n < 0 or s.x+m < 0:
                        continue
                    if mapData[s.y+n][s.x+m] is not "0":
                        s_prime = Node.Location(s.x+m, s.y+n)
                        if exist.has_key(s_prime.key()) is False:
                            exist[s_prime.key()] = True
                            gValue[s_prime.key()] = float('inf')
                        temp_gValue = gValue[s.key()] + distance(s, s_prime)
                        if temp_gValue < gValue[s_prime.key()]:
                            gValue[s_prime.key()] = temp_gValue
                            parent[s_prime.key()] = s

                            if closedArray[0].has_key(s_prime.key()) is False :
                                fringeArray[0].insert(s_prime, gValue[s_prime.key()]+w1*heuristicArray[i].hValue(s_prime,goal))
                                for i in range(1, len(heuristicArray)):
                                    if closedArray[i].has_key(s_prime.key()) is False:
                                        fringeArray[i].insert(s_prime, gValue[s_prime.key()]+w1*heuristicArray[i].hValue(s_prime,goal))


def findPath(current, i):
    path_id = []
    parent = parentArray[i]
    path_id.append(current)
    while parent.has_key(current.key()):
        path_id.append(parent[current.key()])
        current = parent[current.key()]
    return path_id

def output(target):
    fringe = fringeArray[result_i]
    closed = closedArray[result_i]
    if fringe.has(target) is True:
        print(fringe.getLoc(target.key()))
    elif closed.has_key(target.key()):
        print(closed[target.key()])

def distance(s, s_prime):
    # print mapData[s.y][s.x], mapData[s_prime.y][s_prime.x]
    distConst= sqrt((s.x- s_prime.x)**2+(s.y- s_prime.y)**2)
    if mapData[s.y][s.x] == '1':
        if mapData[s_prime.y][s_prime.x] == '1':
            dist =distConst
        elif mapData[s_prime.y][s_prime.x] == '2':
            dist =1.5* distConst
        elif 'a' in mapData[s_prime.y][s_prime.x]:
            dist =distConst
        elif 'b' in mapData[s_prime.y][s_prime.x]:
            dist =1.5* distConst
    elif mapData[s.y][s.x] == '2':
        if mapData[s_prime.y][s_prime.x] == '1':
            dist =1.5* distConst
        elif mapData[s_prime.y][s_prime.x] == '2':
            dist =2* distConst
        elif 'a' in mapData[s_prime.y][s_prime.x]:
            dist =1.5* distConst
        elif 'b' in mapData[s_prime.y][s_prime.x]:
            dist =2* distConst
    elif 'a' in mapData[s.y][s.x]:
        if mapData[s_prime.y][s_prime.x] == '1':
            dist =distConst
        elif mapData[s_prime.y][s_prime.x] == '2':
            dist =1.5* distConst
        elif 'a' in mapData[s_prime.y][s_prime.x]:
            if distConst >1:
                dist= distConst
            else:
                dist =0.25* distConst
        elif 'b' in mapData[s_prime.y][s_prime.x]:
            if distConst >1:
                dist= 1.5* distConst
            else:
                dist =0.375* distConst
    elif 'b' in mapData[s.y][s.x]:
        if mapData[s_prime.y][s_prime.x] == '1':
            dist =1.5* distConst
        elif mapData[s_prime.y][s_prime.x] == '2':
            dist =2* distConst
        elif 'a' in mapData[s_prime.y][s_prime.x]:
            if distConst > 1:
                dist= 1.5* distConst
            else:
                dist =0.375* distConst
        elif 'b' in mapData[s_prime.y][s_prime.x]:
            if distConst >1:
                dist= 2* distConst
            else:
                dist =0.5* distConst
    #dist =sqrt((s.x- s_prime.x)**2+(s.y- s_prime.y)**2)
    return dist
