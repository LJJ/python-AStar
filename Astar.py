__author__ = 'SiyuChen and lujiji'
from math import *
import BinaryHeap
import Node


fringeArray = []#BinaryHeap.BinaryHeap()
closedArray = []
mapData = None
parentArray = []
hValueArray = []
fValueArray = []
gValueArray = []

def resetAllData():
    global fringeArray
    fringeArray = [BinaryHeap.BinaryHeap()]
    global closedArray
    closedArray = [{}]
    global parentArray
    parentArray = [{}]
    global gValueArray
    gValueArray = [{}]
    global hValueArray
    hValueArray = [{}]
    global fValueArray
    fValueArray = [{}]

def Astar(sStart, sGoal, mapD, wa):
    # A-star algorithm
    resetAllData()
    global mapData
    mapData = mapD

    cost = 0.0
    gValue = gValueArray[0]
    hValue = hValueArray[0]
    fValue = fValueArray[0]
    parent = parentArray[0]
    fringe = fringeArray[0]
    closed = closedArray[0]

    def findPath(current):
        path_id.append(current)
        while parent.has_key(current.key()):
            path_id.append(parent[current.key()])
            current = parent[current.key()]

    w=wa
    gValue[sStart.key()] = 0.0
    hValue[sStart.key()] = hFunc(sStart, sGoal)
    fValue[sStart.key()] = w*hFunc(sStart, sGoal)
    fringe.insert(sStart, fValue[sStart.key()])
    path_id=[]
    while fringe.count() > 0:
        s = fringe.pop()
        if s == sGoal:
            print "path found"
            cost = s.fValue
            print "cost: %f" % (cost)
            loc1 = findPath(s)
            break
        #temp_fValue = fValue.pop(s)
        closed[s.key()] = s
        for i in range(-1,2):
            for j in range(-1,2):
                if not(i == 0 and j == 0):
                    if s.y+j > 119 or s.x+i > 159 or s.y+j < 0 or s.x+i < 0:
                        continue
                    if mapData[s.y+j][s.x+i] is not "0":
                        s_prime = Node.Location(s.x+i, s.y+j)
                        if closed.has_key(s_prime.key()) is False:
                            temp_gValue = gValue[s.key()] + distance(s, s_prime)
                            if fringe.has(s_prime) is False:
                                s_prime.fValue = float('inf')
                                s_prime.parent = None
                                status = True
                            else:
                                s_prime = fringe.getLoc(s_prime.key())  #don't remove
                                if temp_gValue < gValue[s_prime.key()]:
                                    status = True
                                else:
                                    status = False
                            if status == True:
                                parent[s_prime.key()] = s
                                gValue[s_prime.key()] = temp_gValue
                                hValue[s_prime.key()] = hFunc(s_prime,sGoal)
                                fValue[s_prime.key()] = gValue[s_prime.key()]+w*hValue[s_prime.key()]
                                fringe.insert(s_prime, fValue[s_prime.key()])
    return path_id, cost


def seqAStar():
    resetAllData()

def output(target):
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

def hFunc(current, goal):
    hValue = 0.25 * (abs(current.x - goal.x) + abs(current.y - goal.y))
    # hValue = (sqrt(2)-1)*min(abs(current.x - goal.x), abs(current.y - goal.y))+ max(abs(current.x - goal.x), abs(current.y - goal.y))
    # hValue = abs(current.x - goal.x) + abs(current.y - goal.y)
    # hValue = sqrt((current.x - goal.x)**2 + (current.y - goal.y)**2)
    # hValue = 2*((sqrt(2)-1)*min(abs(current.x - goal.x), abs(current.y - goal.y))+ max(abs(current.x - goal.x), abs(current.y - goal.y)))
    return hValue
