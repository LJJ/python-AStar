__author__ = 'lujiji and SiyuChen'
#import Map
from Map import *
from Astar import *

import random

createMap()
readMap()
start_x, start_y, goal_x, goal_y = CreateStartGoal()

print mapData[start_y][start_x], start_x, start_y
print mapData[goal_y][goal_x], goal_x, goal_y
sStart = (start_x, start_y)
sGoal = (goal_x, goal_y)


path_id = Astar(sStart, sGoal, mapData)
print path_id

DrawLines(path_id[len(path_id)-1], sStart)
for i in range(0, len(path_id)-1):
    DrawLines(path_id[i], path_id[i+1])

mainloop()


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
