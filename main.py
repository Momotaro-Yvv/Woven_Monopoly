import sys
import json

class Player():
    def __init__(self,name):
        self.name = name
        self.money = 16
        self.properties = []
        self.position = "Go"

class Property():
    def __init__(self, propertyName, positionIndex, color, rent, owner):
        self.propertyName = propertyName
        self.position = positionIndex
        self.color = color
        self.rent = rent
        self.owner = owner
    def __str__(self) -> str:
        return (self.propertyName 
        + "\nColour: " + self.color
        + "\nRent: " + str(self.rent)
        + "\nOwner: " + str(self.owner)
        +"\n-----------------------")
    def setOwner(self, newOwner):
        self.owner = owner = newOwner

class Go():
    def __init__(self,positionIndex):
        self.position = positionIndex
    
    def __str__(self):
        return "\nGo\n-----------------------"

class Board():
    def __init__(self, filename):

        # Read file
        with open(filename) as f:
            contents = json.load(f)

        self.cells = []
        # Validate board file format & missing info
        for i, cell in enumerate(contents):
            cellName = cell["name"]
            cellType = cell["type"]

            if cellType == "go":
                goCell = Go(i)
                self.cells.append(goCell)
            elif cellType == "property":
                propertyName = cellName
                colour = cell["colour"]
                rent = cell["price"]
                owner = None
                propertyCell = Property(propertyName,i,colour,rent,owner)
                self.cells.append(propertyCell)
            else:
                raise Exception("Board file contains wrong types")
    
    def print(self):
        for cell in self.cells:
                print(cell)
            
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


def parseArgs():

    # check args format
    if len(sys.argv) != 3:
        sys.exit("Wrong arguments.\nUsage: python3 main.py board.json rolls.json")
    else:
        board_file = sys.argv[1]
        rolls_file = sys.argv[2]
        
        try:
            board = Board(board_file)
            roller = Roller(rolls_file)

            print("Board:")
            board.print()

            # print("Rollers:")
            # roller.print()
        except:
            sys.exit("File Not Found.\nUsage: python3 main.py board.json rolls.json")
    return board,roller

def checkWinner():
    return True

'''
Main Entry point
''' 

board,roller = parseArgs()

Peter = Player("Peter")
Billy = Player("Billy")
Charlotte = Player("Charlotte")
Sweedal = Player("Sweedal")






