__author__ = 'SiyuChen and lujiji'
from math import *
import BinaryHeap
import time
import Node


fringe = BinaryHeap.BinaryHeap()
closed = {}

def Astar(sStart, sGoal, mapData):
    # A-star algorithm
    def hFunc(current, goal):
        hValue =(sqrt(2)-1)*min(abs(current.x - goal.x), abs(current.y- goal.y))+ max(abs(current.x- goal.x), abs(current.y- goal.y))
        return hValue

    #print mapData

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

    def findPath(current):
        path_id.append(current)
        while current.parent is not None:
            path_id.append(current.parent)
            current = current.parent

    # Main from here
    cost = 0.0
    #fValue = {}
    w=1.0
    sStart.gValue = 0
    sStart.hValue = hFunc(sStart, sGoal)
    sStart.fValue = w*hFunc(sStart, sGoal)
    fringe.insert(sStart)
    record = False
    #fValue[sStart] = gValue[sStart] + hValue[sStart]
    path_id=[]
    while fringe.count() > 0:
        s = fringe.pop()
        if record is True:
            print(s.key())
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
                        if s_prime == Node.Location(120,97):
                            record = True
                        if closed.has_key(s_prime.key()) is False:
                            temp_gValue = s.gValue + distance(s, s_prime)
                            if fringe.has(s_prime) is False:
                                s_prime.fValue = float('inf')
                                s_prime.parent = None
                                status = True
                            else:
                                s_prime = fringe.getLoc(s_prime.key())
                                if temp_gValue < s_prime.gValue:
                                    status = True
                                else:
                                    status = False
                            if status == True:
                                s_prime.parent = s
                                s_prime.gValue = temp_gValue
                                s_prime.hValue = hFunc(s_prime,sGoal)
                                s_prime.fValue = s_prime.gValue+w*s_prime.hValue
                                fringe.insert(s_prime)
    return path_id, cost

def output(target):
    if fringe.has(target) is True:
        print(fringe.getLoc(target.key()))
    elif closed.has_key(target.key()):
        print(closed[target.key()])
