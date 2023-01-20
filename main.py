import sys
import json

class Player():
    def __init__(self,name, money, properties, position):
        self.name = name
        self.money = money
        self.properties = properties
        self.position = position

class Property():
    def __init__(self, propertyName, color, rent, owner):
        self.propertyName = propertyName
        self.color = color
        self.rent = rent
        self.owner = owner
    def __str__(self) -> str:
        return ("Cell Info: \n"
        + self.propertyName 
        + "\nColour: " + self.color 
        + "\nRent: " + str(self.rent)
        + "\nOwner " + str(self.owner)
        +"\n-----------------------")

class Go():
    def __init__(self):
        pass
    
    def __str__(self) -> str:
        return "\nGo\n-----------------------"


class Board():
    def __init__(self, filename):

        # Read file
        with open(filename) as f:
            contents = json.load(f)

        self.cells = []
        # Validate board file format & missing info
        for cell in contents:
            cellName = cell["name"]
            cellType = cell["type"]

            if cellType == "go":
                goCell = Go()
                self.cells.append(goCell)
            elif cellType == "property":
                propertyName = cellName
                colour = cell["colour"]
                rent = cell["price"]
                owner = None
                propertyCell = Property(propertyName,colour,rent,owner)
                self.cells.append(propertyCell)
            else:
                raise Exception("Board file contains wrong types")
    
    def print(self):
        for cell in self.cells:
            
                print(cell.__str__())
            

class Roller():
    def __init__(self,filename):
        
        # Read file
        with open(filename) as f:
            rollers = json.load(f)

        # Validate rolls file format
        for roller in rollers:
            if not isinstance(roller, int):
                raise Exception("Roller file contains wrong types, prices must be a list of integers!")

        self.rollers = rollers

    def print(self):
        for i, roller in enumerate(self.rollers):
            print(i, roller)

'''
Main Entry point
''' 
# check args format
if len(sys.argv) != 3:
    sys.exit("Wrong arguments.\nUsage: python3 main.py board.json rolls.json")

board_file = sys.argv[1]
rolls_file = sys.argv[2]

board = Board(board_file)
roller = Roller(rolls_file)

print("Board:")
board.print()

# print("Rollers:")
# roller.print()
# print("Solving...")

