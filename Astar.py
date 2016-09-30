__author__ = 'SiyuChen and lujiji'
from math import *

def Astar(sStart, sGoal, mapData):
    # A-star algorithm
    def hFunc(current, goal):
        hValue =(sqrt(2)-1)*min(abs(current[0]- goal[0]), abs(current[1]- goal[1]))+ max(abs(current[0]- goal[0]), abs(current[1]- goal[1]))
        return hValue

    print mapData

    def distance(s, s_prime):
        distConst= sqrt((s[0]- s_prime[0])**2+(s[1]- s_prime[1])**2)
        if mapData[s[1]][s[0]] == '1':
            if mapData[s_prime[1]][s_prime[0]] == '1':
                dist =distConst
            elif mapData[s_prime[1]][s_prime[0]] == '2':
                dist =1.5* distConst
            elif 'a' in mapData[s_prime[1]][s_prime[0]]:
                dist =distConst
            elif 'b' in mapData[s_prime[1]][s_prime[0]]:
                dist =1.5* distConst
        elif mapData[s[1]][s[0]] == '2':
            if mapData[s_prime[1]][s_prime[0]] == '1':
                dist =1.5* distConst
            elif mapData[s_prime[1]][s_prime[0]] == '2':
                dist =2* distConst
            elif 'a' in mapData[s_prime[1]][s_prime[0]]:
                dist =1.5* distConst
            elif 'b' in mapData[s_prime[1]][s_prime[0]]:
                dist =2* distConst
        elif 'a' in mapData[s[1]][s[0]]:
            if mapData[s_prime[1]][s_prime[0]] == '1':
                dist =distConst
            elif mapData[s_prime[1]][s_prime[0]] == '2':
                dist =1.5* distConst
            elif 'a' in mapData[s_prime[1]][s_prime[0]]:
                if distConst >1:
                    dist= distConst
                else:
                    dist =0.25* distConst
            elif 'b' in mapData[s_prime[1]][s_prime[0]]:
                if distConst >1:
                    dist= 1.5* distConst
                else:
                    dist =0.375* distConst
        elif 'b' in mapData[s[1]][s[0]]:
            if mapData[s_prime[1]][s_prime[0]] == '1':
                dist =1.5* distConst
            elif mapData[s_prime[1]][s_prime[0]] == '2':
                dist =2* distConst
            elif 'a' in mapData[s_prime[1]][s_prime[0]]:
                if distConst > 1:
                    dist= 1.5* distConst
                else:
                    dist =0.375* distConst
            elif 'b' in mapData[s_prime[1]][s_prime[0]]:
                if distConst >1:
                    dist= 2* distConst
                else:
                    dist =0.5* distConst
        #dist =sqrt((s[0]- s_prime[0])**2+(s[1]- s_prime[1])**2)
        return dist

    def findPath(path, current):
        locstart=current
        path_id.append(locstart)
        while path[current] in path:
            locend = findPath(path, path[current])
            current = locend
            return locstart

    # Main from here
    fringe = {}
    closed = {}
    path = {}
    gValue = {}
    hValue = {}
    fValue = {}
    gValue[sStart] = 0
    hValue[sStart] = hFunc(sStart, sGoal)
    fringe[sStart]=gValue
    fValue[sStart] = gValue[sStart] + hValue[sStart]
    path_id=[]
    while fringe != {}:
        s = min(fValue.items(), key=lambda x: x[1])[0]
        if s == sGoal:
            print "path found"
            loc1 = findPath(path, sGoal)
            break
        temp_dis = fringe.pop(s)
        temp_fValue = fValue.pop(s)
        closed[s] = temp_dis
        for i in range(-1,2):
            for j in range(-1,2):
                if not(i == 0 and j == 0):
                    if mapData[s[1]+j][s[0]+i] is not "0":
                        s_prime = (s[0]+i, s[1]+j)
                        if s_prime not in closed:
                            temp_gValue = gValue[s] + distance(s, s_prime)
                            if s_prime not in fringe:
                                fringe[s_prime] = temp_gValue
                                status = True
                            elif temp_gValue < gValue[s_prime]:
                                status = True
                            else:
                                status = False
                            if status == True:
                                path[s_prime] = s
                                gValue[s_prime] = temp_gValue
                                hValue[s_prime] = hFunc(s_prime, sGoal)
                                fValue[s_prime] = gValue[s_prime] + hValue[s_prime]
    return path_id

