__author__ = 'lujiji'



class Location:
    x = 0
    y = 0
    onBoundary = False
    fValue = 0.0
    index = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    # def __init__(self, loc):
    #     self.x = loc.x
    #     self.y = loc.y
    #     self.fValue = loc.fValue

    def __str__(self):
        return "Location (%s,%s)\n f-value%.1f" % (self.x,self.y, self.fValue)

    # def fValue(self):
    #     return self.gValue + self.hValue

    def key(self):
        return "%d,%d" % (self.x,self.y)


    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        else :
            return False

