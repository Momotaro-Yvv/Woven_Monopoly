import sys
import json

class Player():
    def __init__(self,name):
        self.name = name
        self.money = 16
        self.properties = []
        self.position = 0
    def __str__(self):
        return (self.name 
            + "\nMoney: " + str(self.money)
            + "\nOwns properties: " + str(self.properties)
            + "\nCurrently at: " + str(self.position))
    def move(self, steps):
        self.position += steps
    def purchaseProperty(self, propertyName):
         self.properties.append(propertyName)
    def payRent(self,rent):
        self.money -= rent
    def ifBankrupt(self):
        return self.money <= 0
    
class Property():
    def __init__(self, propertyName, positionIndex, color, price, owner):
        self.propertyName = propertyName
        self.position = positionIndex
        self.color = color
        self.price = price
        self.owner = owner
    def __str__(self) -> str:
        return (self.propertyName 
            + "\nColour: " + self.color
            + "\Price: " + str(self.price)
            + "\nOwner: " + str(self.owner)
            +"\n-----------------------")
    def setOwner(self, newOwner):
        self.owner = newOwner

class Go():
    def __init__(self,positionIndex):
        self.name = "Go"
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
                price = cell["price"]
                owner = None
                propertyCell = Property(propertyName,i,colour,price,owner)
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
                sys.exit("Roller file contains wrong types, prices must be a list of integers!")

        self.rollers = rollers

    def __str__(self):
        return str(self.rollers)
    def isEmpty(self):
        return len(self.rollers) == 0
    def getNextRoll(self):
        if self.isEmpty():
            raise Exception("Not enough rollers in the defined file.")
        else:
            nextRoll = self.rollers[0]
            self.rollers = self.rollers[1:]
            return nextRoll

#TODO: refine this function, make it accept user args in random order, e.g. -board board.file -roller roller.file
def parseArgs():

    # check args format
    if len(sys.argv) != 3:
        sys.exit("Wrong number of arguments.\nUsage: python3 main.py board.json rolls.json")
    
    else:
        board_file = sys.argv[1]
        rolls_file = sys.argv[2]
        
        try:
            board = Board(board_file)
            print("Board:")
            board.print()

        except:
            sys.exit("Board file Not Found. Please check again. \nUsage: python3 main.py board.json rolls.json")
        
        try:
            roller = Roller(rolls_file)
            print("Rollers:")
            print(roller)
        except:
            sys.exit("Roller file Not Found. Please check again. \nUsage: python3 main.py board.json rolls.json")
       
    return board,roller

def checkWinner():
    winner = None
    currentPlayersMoney = []
    for player in players:  
        currentPlayersMoney.append(player.money)
    for player in players:
        if player.ifBankrupt():
            winner = [players[index] for index, money in enumerate(currentPlayersMoney) if money == max(currentPlayersMoney)]
    print("checking Winner:",currentPlayersMoney, winner)
    return winner

'''
Main Entry point
''' 
if __name__ == "__main__":
    board,roller = parseArgs()

    peter = Player("Peter")
    billy = Player("Billy")
    charlotte = Player("Charlotte")
    sweedal = Player("Sweedal")
    players = [peter,billy,charlotte,sweedal]
    playerIndex = 0
    totalNumOfCells = len(board.cells)

    while not checkWinner():
        nextPlayer = players[playerIndex%4]
        playerIndex += 1

        nextRoll = roller.getNextRoll()

        timesPassGo = (nextPlayer.position+ nextRoll) // totalNumOfCells
        nextPlayer.position = (nextPlayer.position+ nextRoll) % totalNumOfCells
        nextPlayer.money += timesPassGo
        
        print("-------------------------\n" + nextPlayer.name)
        print("Rolled: " + str(nextRoll))

        if isinstance(board.cells[nextPlayer.position],Go):
            print("Now at Go, gain $1")
            nextPlayer.money += 1
        else:
            print("Now at: " + board.cells[nextPlayer.position].propertyName)
            # step on a property
            thisProperty = board.cells[nextPlayer.position]
            if thisProperty.owner == None:
                nextPlayer.properties.append(thisProperty)
                nextPlayer.money -= thisProperty.price
                thisProperty.setOwner(nextPlayer)

            else:
                # this property has owned by someone
                if thisProperty.owner.name == nextPlayer.name:
                    continue
                else:
                    thisProperty.owner.money += thisProperty.price
                    nextPlayer.money -= thisProperty.price


    for player in players:
        print(player)

    print(checkWinner)
