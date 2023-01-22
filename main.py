import sys
import json

class Player():
    def __init__(self,name):
        self.name = name
        self.money = 16
        self.properties = []
        self.position = 0
    def __str__(self):
        propertiesList = [str(p) for p in self.properties]
        return (self.name 
            , "\nMoney: ", self.money
            , "\nOwns properties: ", propertiesList
            , "\nCurrently at: ", self.position)
    def move(self, steps):
        self.position += steps
    def purchaseProperty(self, propertyName):
         self.properties.append(propertyName)
    def payRent(self,rent):
        self.money -= rent
    def ifBankrupt(self):
        return self.money <= 0
    
class Property():
    def __init__(self, propertyName, positionIndex, colour, price, owner):
        self.propertyName = propertyName
        self.position = positionIndex
        self.colour = colour
        self.price = price
        self.owner = owner
    def __str__(self) -> str:
        return (self.propertyName 
            + "\nColour: " + self.colour
            + "\nPrice: " + str(self.price)
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
        self.properties_Set = {}

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
                property = Property(propertyName,i,colour,price,owner)
                self.cells.append(property)

                if property.colour not in self.properties_Set:
                    self.properties_Set[property.colour] = property
                else:
                    self.properties_Set[property.colour] = [self.properties_Set[property.colour],property]
                
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
    winners = None
    currentPlayersMoney = []
    for player in players:  
        currentPlayersMoney.append(player.money)
    for player in players:
        if player.ifBankrupt():
            winners = [players[index] for index, money in enumerate(currentPlayersMoney) if money == max(currentPlayersMoney)]
    
    
    print("checking Winner:",currentPlayersMoney)
    return winners

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

    print(board.properties_Set)

    while not checkWinner():
        nextPlayer = players[playerIndex%4]
        playerIndex += 1

        nextRoll = roller.getNextRoll()

        timesPassGo = (nextPlayer.position+ nextRoll) // totalNumOfCells
        nextPlayer.position = (nextPlayer.position+ nextRoll) % totalNumOfCells
        nextPlayer.money += timesPassGo

        print("-------------------------\n" + nextPlayer.name)
        print("Rolled: " + str(nextRoll))
        if timesPassGo > 0:
             print(nextPlayer.name, "Passing Go, gain $1")

        if isinstance(board.cells[nextPlayer.position],Go):
            print("Now at Go, gain $1")
            nextPlayer.money += 1
        else:
            # step on a property
            print("Now at: " + board.cells[nextPlayer.position].propertyName)
            thisProperty = board.cells[nextPlayer.position]
            
            if thisProperty.owner == None:
                nextPlayer.properties.append(thisProperty)
                nextPlayer.money -= thisProperty.price
                thisProperty.setOwner(nextPlayer)
                print(nextPlayer.name, "Now successfully purchase the property",thisProperty.propertyName)

            else:
                # this property has owned by someone
                if thisProperty.owner.name == nextPlayer.name:
                    print("This property has already owned by", nextPlayer.name)
                    continue
                else:
                    print(nextPlayer.name, "paying", thisProperty.owner.name, thisProperty.price)
                    
                    #check if the whole set owned by same player, if yes double the  price
                    rent = thisProperty.price
                    colourSet = thisProperty.colour
                    propertiesSet = board.properties_Set[colourSet]
                    
                    owners = []
                    for p in propertiesSet:
                        if p.owner is None:
                            continue
                        else:
                            owners.append(p.owner)
                    if all(element == owners[0] for element in owners):
                        rent = rent * 2
                    thisProperty.owner.money += rent
                    nextPlayer.money -= rent


    winners = checkWinner()
    print([winner.name for winner in winners])
