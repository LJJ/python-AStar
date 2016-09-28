__author__ = 'lujiji'


class Node:
    x = 0
    y = 0
    unit = 0.0
    color = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y


class HardNode(Node):
    color = 0


class FastNode(Node):
    color = 1


class ForbiddenNode(Node):
    color = 2