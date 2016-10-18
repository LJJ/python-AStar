__author__ = 'lujiji'
import Map
import copy
# from __future__ import division

class BinaryHeap:
    def __init__(self):
        self.heap = [Map.Location(0,0)]
        self.check = {}
        self.fValue = {}

    def insert(self, aLoc, fValue):
        loc = copy.copy(aLoc)
        self.fValue[loc.key()] = fValue
        if self.has(loc) is False:
            self.check[loc.key()] = loc
            self.heap.append(loc)
            loc.index = len(self.heap) - 1
            self.up(loc.index)
        else:
            self.reorder(loc)

    def count(self):
        return len(self.heap) - 1

    def reorder(self, loc):
        target = self.check[loc.key()]
        self.up(target.index)


    def up(self, i):
        cldIndex = i
        while cldIndex//2 > 0:
            parIndex = cldIndex//2
            if self.fValue[self.heap[cldIndex].key()] < self.fValue[self.heap[parIndex].key()]:
                tmp = self.heap[cldIndex]
                self.heap[cldIndex] = self.heap[parIndex]
                self.heap[parIndex] = tmp
                self.heap[parIndex].index = parIndex
                self.heap[cldIndex].index = cldIndex
                cldIndex = parIndex
            else:
                break

    def pop(self):
        if len(self.heap) > 1:
            result = self.heap[1]
            self.heap[1] = self.heap[-1]
            self.heap[1].index = 1
            self.heap.pop()
            self.down(1)
            self.check.pop(result.key())

            return result

    def remove(self, loc):
        if self.has(loc) is True:
            target = self.check[loc.key()]
            self.heap[-1].index = target.index
            self.heap[target.index] = self.heap[-1]
            self.heap.pop()
            self.check.pop(target.key())
            self.down(target.index)

    def minValue(self):
        if len(self.heap) > 1:
            return self.fValue[self.heap[1].key()]

    def down(self,i):
        parIndex = i
        while parIndex*2 <= len(self.heap) - 1:
            minChild =self.minChild(parIndex)
            if self.fValue[self.heap[parIndex].key()] > self.fValue[self.heap[minChild].key()]:
                tmp = self.heap[parIndex]
                self.heap[parIndex] = self.heap[minChild]
                self.heap[minChild] = tmp
                self.heap[parIndex].index = parIndex
                self.heap[minChild].index = minChild
                parIndex = minChild

            else:
                break


    def minChild(self,parIndex):
        if parIndex*2+1 > len(self.heap) - 1:
            return parIndex*2
        else:
            if self.fValue[self.heap[parIndex*2].key()]>self.fValue[self.heap[parIndex*2+1].key()]:
                return parIndex*2+1
            else:
                return parIndex*2




    def has(self, other):
        return self.check.has_key(other.key())

    def getLoc(self, key):
         return self.check[key]

    def getFvalue(self, loc):
        return self.fValue[loc.key()]

