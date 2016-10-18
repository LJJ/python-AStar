__author__ = 'SiyuChen and lujiji'
from math import *
import BinaryHeap
import Node
from Heuristic import *

heuristicArray = [HeuristicOptimal,HeuristicOne,HeuristicTwo,HeuristicThree,HeuristicFour]

class Astar():

    fringeArray = []
    closedArray = []
    mapData = None
    parentArray = []
    gValueArray = []
    exist = {}


    def __init__(self, mapData, w1 = 1.0, w2 = 1.0):
        amount = len(heuristicArray)
        self.fringeArray = [BinaryHeap.BinaryHeap() for i in range(amount)]
        self.closedArray = [{} for i in range(amount)]
        self.parentArray = [{} for i in range(amount)]
        self.gValueArray = [{} for i in range(amount)]
        self.exist = {}
        self.mapData = mapData
        self.result_i = 0
        self.w1 = w1
        self.w2 = w2
        self.valueDic = [{} for i in range(amount)]



    def execute(self, sStart, sGoal):
        # A-star algorithm
        cost = 0.0
        gValue = self.gValueArray[0]
        parent = self.parentArray[0]
        fringe = self.fringeArray[0]
        closed = self.closedArray[0]

        gValue[sStart.key()] = 0.0
        fringe.insert(sStart, HeuristicOptimal.hValue(sStart, sGoal))
        path_id = []

        while fringe.count() > 0:
            s = fringe.pop()
            if s == sGoal:
                print "path found"
                cost = 0.0#s.fValue
                print "cost: %f" % (cost)
                path_id = self.findPath(s,0)
                break
            closed[s.key()] = s
            self.expand(s,sGoal,0)
        return path_id, cost, 0

    def expand(self, s, goal, i):
        gValue = self.gValueArray[i]
        parent = self.parentArray[i]
        fringe = self.fringeArray[i]
        closed = self.closedArray[i]
        previousMinValue = 0
        closed[s.key()] = s
        for m in range(-1,2):
                for n in range(-1,2):
                    if not(m == 0 and n == 0):
                        if s.y+n > 119 or s.x+m > 159 or s.y+n < 0 or s.x+m < 0:
                            continue
                        if self.mapData[s.y+n][s.x+m] is not "0":
                            s_prime = Node.Location(s.x+m, s.y+n)
                            if closed.has_key(s_prime.key()) is False:
                                temp_gValue = gValue[s.key()] + self.distance(s, s_prime)
                                if fringe.has(s_prime) is False:
                                    gValue[s_prime.key()] = float('inf') #warning
                                    status = True
                                else:
                                    if temp_gValue < gValue[s_prime.key()]:
                                        status = True
                                    else:
                                        status = False
                                if status == True:
                                    parent[s_prime.key()] = s
                                    gValue[s_prime.key()] = temp_gValue
                                    fValue_i =  gValue[s_prime.key()]+self.w1*heuristicArray[i].hValue(s_prime,goal)
                                    self.saveValue( i,s_prime,temp_gValue,fValue_i)
                                    fringe.insert(s_prime, fValue_i)

    def saveValue(self,i, loc, gValue, fValue):
        self.valueDic[i][loc.key()] = "gValue: %.2f hValue: %.2f fValue: %.2f" % (gValue, fValue-gValue, fValue)

    def findPath(self, current, i):
        path_id = []
        parent = self.parentArray[i]
        path_id.append(current)
        while parent.has_key(current.key()):
            path_id.append(parent[current.key()])
            current = parent[current.key()]
        return path_id

    def output(self, target):
        print(target)
        if self.valueDic[self.result_i].has_key(target.key()):
            print(self.valueDic[self.result_i][target.key()])

    def distance(self, s, s_prime):
        # print mapData[s.y][s.x], mapData[s_prime.y][s_prime.x]
        distConst= sqrt((s.x- s_prime.x)**2+(s.y- s_prime.y)**2)
        mapData = self.mapData
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

class AstarSeq(Astar):

    def execute(self, sStart, sGoal):
        # A-star algorithm
        numNodes = 0
        for i in range(0,len(heuristicArray)):
            self.gValueArray[i][sStart.key()] = 0.0
            self.gValueArray[i][sGoal.key()] = float('inf')
            self.fringeArray[i].insert(sStart,self.w1*heuristicArray[i].hValue(sStart,sGoal))

        while self.fringeArray[0].minValue() < float('inf'):
            numNodes += 1
            for i in range(1, len(heuristicArray)):
                if self.fringeArray[i].minValue() <= self.w2*self.fringeArray[0].minValue():
                    if self.gValueArray[i][sGoal.key()] < self.fringeArray[i].minValue():
                        if self.gValueArray[i][sGoal.key()] < float('inf'):
                            path_id = self.findPath(sGoal, i)
                            self.result_i = i
                            return path_id, self.fringeArray[i].getFvalue(sGoal), numNodes
                    else:
                        s = self.fringeArray[i].pop()
                        self.expand(s,sGoal,i)
                else:
                    if self.gValueArray[0][sGoal.key()] <= self.fringeArray[0].minValue():
                        if self.gValueArray[0][sGoal.key()] < float('inf'):
                            path_id =self.findPath(sGoal, 0)
                            self.result_i = 0
                            return path_id, self.fringeArray[0].getFvalue(sGoal), numNodes
                    else:
                        s = self.fringeArray[0].pop()
                        self.expand(s,sGoal,0)
        return [], self.fringeArray[0].getFvalue(sGoal), numNodes



class AstarInt(Astar):


    def execute(self, sStart, sGoal):
        self.gValueArray[0][sStart.key()] = 0.0
        self.gValueArray[0][sGoal.key()] = float('inf')
        self.exist[sStart.key()] = True
        numNodes = 0
        for i in range(0,len(heuristicArray)):
            self.fringeArray[i].insert(sStart,self.w1*heuristicArray[i].hValue(sStart,sGoal))

        while self.fringeArray[0].minValue() < float('inf'):
            numNodes += 1
            for i in range(1, len(heuristicArray)):
                if self.fringeArray[i].minValue() <= self.w2*self.fringeArray[0].minValue():
                    if self.gValueArray[0][sGoal.key()] <= self.fringeArray[i].minValue():
                        if self.gValueArray[0][sGoal.key()] < float('inf'):
                            path_id = self.findPath(sGoal, 0)
                            return path_id, self.fringeArray[0].getFvalue(sGoal), numNodes
                    else:
                        s = self.fringeArray[i].pop()
                        self.expand(s,sGoal)
                        self.result_i = i
                        self.closedArray[1][s.key()] = s
                else:
                    if self.gValueArray[0][sGoal.key()] <= self.fringeArray[0].minValue():
                        if self.gValueArray[0][sGoal.key()] < float('inf'):
                            path_id =self.findPath(sGoal, 0)
                            self.result_i = 0
                            return path_id, self.fringeArray[0].getFvalue(sGoal), numNodes
                    else:
                        s = self.fringeArray[0].pop()
                        self.expand(s,sGoal)
                        self.closedArray[0][s.key()] = s
        return [], self.fringeArray[0].getFvalue(sGoal), numNodes

    def expand(self, s, goal):
        gValue = self.gValueArray[0]
        for i in range(len(self.fringeArray)):
            self.fringeArray[i].remove(s)

        parent = self.parentArray[0]
        # closed = closedArray[i]
        for m in range(-1,2):
                for n in range(-1,2):
                    if not(m == 0 and n == 0):
                        if s.y+n > 119 or s.x+m > 159 or s.y+n < 0 or s.x+m < 0:
                            continue
                        if self.mapData[s.y+n][s.x+m] is not "0":
                            s_prime = Node.Location(s.x+m, s.y+n)
                            if self.exist.has_key(s_prime.key()) is False:
                                self.exist[s_prime.key()] = True
                                gValue[s_prime.key()] = float('inf')
                            temp_gValue = gValue[s.key()] + self.distance(s, s_prime)
                            if temp_gValue < gValue[s_prime.key()]:
                                gValue[s_prime.key()] = temp_gValue
                                parent[s_prime.key()] = s

                                if self.closedArray[0].has_key(s_prime.key()) is False :
                                    fValue_zero =  gValue[s_prime.key()]+self.w1*heuristicArray[0].hValue(s_prime,goal)
                                    self.fringeArray[0].insert(s_prime, fValue_zero)
                                    self.saveValue(0,s_prime,gValue[s_prime.key()],fValue_zero)
                                    if self.closedArray[1].has_key(s_prime.key()) is False:
                                        for i in range(1, len(heuristicArray)):
                                            fValue_i = gValue[s_prime.key()] + self.w1*heuristicArray[i].hValue(s_prime,goal)
                                            if fValue_i <= self.w2*fValue_zero:
                                                self.fringeArray[i].insert(s_prime, fValue_i)
                                                self.saveValue(0,s_prime,gValue[s_prime.key()],fValue_i)

