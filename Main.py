__author__ = 'lujiji and SiyuChen'
import Map
from Astar import *

import time

start = time.clock()

mapData = Map.readMap()
# createMap()
startLoc, goalLoc = Map.Location(140,104), Map.Location(1,10)#Map.CreateStartGoal(mapData)
print mapData[startLoc.y][startLoc.x], startLoc.x, startLoc.y
print mapData[goalLoc.y][goalLoc.x], goalLoc.x, goalLoc.y

path_id, cost = Astar(startLoc, goalLoc, mapData)
path_id.append(startLoc)
path_id.reverse()
# print path_id
# for i in range(0, len(path_id)):
#     print(str(path_id[i]))
Map.savePath(path_id, cost)

for i in range(0, len(path_id)-1):
    Map.DrawLines(path_id[i], path_id[i+1])

end = time.clock()
print 'Running time is:', end-start

Map.mainloop()

x = 0
# while x != 6:
#     display = ["Please input your choice:",
#                "1. Create new map",
#                "2. Read map from file",
#                "3. Execute A* (WA* etc)",
#                "4. Save result in file",
#                "5. Save map in file",
#                "6. Exit",
#                "Enter your choice:",
#                ]


    # x = input("\n".join(display))
    #
    # if x == 1:
    #     Map.createMap()
    # elif x == 2:
    #     Map.readMap()
    # elif x == 4:
    #     Map.saveMap()
    # else:
    #     print"Wrong number!"
    #     continue
