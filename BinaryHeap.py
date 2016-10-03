__author__ = 'lujiji'
import Map
from __future__ import division

class BinaryHeap:
    def __init__(self):
        self.heap = [0]

    def insert(self, loc):
        self.heap.append(loc)
        self.up()


    def up(self):
        cldIndex = len(self.heap) - 1
        while cldIndex//2 > 0:
            parIndex = cldIndex//2
            if self.heap[cldIndex] < self.heap[parIndex]:
                tmp = self.heap[parIndex]
                self.heap[parIndex] = self.heap[cldIndex]
                self.heap[cldIndex] = tmp
                cldIndex = parIndex
            else:
                break

    def pop(self):
        if len(self.heap) > 1:
            result = self.heap[1]
            self.heap[1] = self.heap[-1]
            self.heap.pop()
            self.down()
            return result

    def down(self):
        parIndex = 1
        while parIndex*2 <= len(self.heap) - 1:
            minChild =self.minChild(parIndex)
            if self.heap[parIndex] > self.heap[minChild]:
                tmp = self.heap[parIndex]
                self.heap[parIndex] = self.heap[minChild]
                self.heap[minChild] = tmp
                parIndex = minChild
            else:
                break


    def minChild(self,parIndex):
        if parIndex*2+1 > len(self.heap) - 1:
            return parIndex*2
        else:
            if self.heap[parIndex*2]>self.heap[parIndex*2+1]:
                return parIndex*2+1
            else:
                return parIndex*2



