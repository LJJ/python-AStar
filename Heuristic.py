__author__ = 'lujiji'
from Node import Location
from math import *


class Heuristic():

    def __init__(self):
        pass

    @staticmethod
    def hValue(current, goal):
        return 0.0

class HeuristicOptimal(Heuristic):
    @staticmethod
    def hValue(current, goal):
        return 0.25 * (abs(current.x - goal.x) + abs(current.y - goal.y))

class HeuristicOne(Heuristic):
    @staticmethod
    def hValue(current, goal):
        return (sqrt(2)-1)*min(abs(current.x - goal.x), abs(current.y - goal.y))+ max(abs(current.x - goal.x), abs(current.y - goal.y))

class HeuristicTwo(Heuristic):
    @staticmethod
    def hValue(current, goal):
        return abs(current.x - goal.x) + abs(current.y - goal.y)

class HeuristicThree(Heuristic):
    @staticmethod
    def hValue(current, goal):
        return sqrt((current.x - goal.x)**2 + (current.y - goal.y)**2)

class HeuristicFour(Heuristic):
    @staticmethod
    def hValue(current, goal):
        return 2*((sqrt(2)-1)*min(abs(current.x - goal.x), abs(current.y - goal.y))+ max(abs(current.x - goal.x), abs(current.y - goal.y)))