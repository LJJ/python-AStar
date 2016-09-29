__author__ = 'lujiji'
import Map

x = 0

while x != 6:
    display = ["Please input your choice:",
               "1. Create new map",
               "2. Read map from file",
               "3. Execute A* (WA* etc)",
               "4. Save result in file",
               "5. Save map in file",
               "6. Exit",
               "Enter your choice:",
               ]

    x = input("\n".join(display))

    if x == 1:
        Map.createMap()
    elif x == 2:
        Map.readMap()
    elif x == 4:
        Map.saveMap()
    else:
        print"Wrong number!"
        continue