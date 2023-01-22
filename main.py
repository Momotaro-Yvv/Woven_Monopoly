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

    def move(self, steps, totalNumOfCells):
        self.position = (self.position+ steps) % totalNumOfCells

    def purchaseProperty(self, thisProperty):
        self.properties.append(thisProperty)
        self.money -= thisProperty.price
        thisProperty.setOwner(self)

    def payRent(self,other_player,rent):
        self.money -= rent
        other_player.money += rent

    def ifBankrupt(self):
        return self.money < 0
    
class Property():
    def __init__(self, propertyName, positionIndex, colour, price, owner):
        self.name = propertyName
        self.position = positionIndex
        self.colour = colour
        self.price = price
        self.owner = owner
    def __str__(self) -> str:
        return (self.name 
            , "\nColour: ",self.colour
            , "\nPrice: ", self.price
            , "\nOwner: ", self.owner
            , "\n-----------------------")
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
            # print("Board:")
            # board.print()

        except:
            sys.exit("Board file Not Found. Please check again. \nUsage: python3 main.py board.json rolls.json")
        
        try:
            roller = Roller(rolls_file)
            # print("Rollers:")
            # print(roller)
        except:
            sys.exit("Roller file Not Found. Please check again. \nUsage: python3 main.py board.json rolls.json")
       
    return board,roller

def gameEnd():
    ifEnd = False
    for player in players:
        if player.ifBankrupt():
            ifEnd = True
    return ifEnd

def welcome_page():
    print("\nWelcome to the Woven Monopoly!")
    print("----------------------------------------------------------")
    print("In Woven Monopoly, the rules of the game are:")
    print("There are four players who take turns in the following order:")
    print("   * Peter")
    print("   * Billy")
    print("   * Charlotte")
    print("   * Sweedal")
    print("      -The dice rolls are set ahead of time, therefore the game is deterministic")
    print("      -Each player starts with $16")
    print("      -Everybody starts on GO")
    print("      -You get $1 when you pass GO (this excludes your starting move)")
    print("      -If you land on a property, you must buy it")
    print("      -If you land on an owned property, you must pay rent to the owner")
    print("      -If the same owner owns all property of the same colour, the rent is doubled")
    print("      -Once someone is bankrupt, whoever has the most money remaining is the winner")
    print("      -There are no chance cards, jail or stations")
    print("      -The board wraps around (i.e. you get to the last space, the next space is the first space)")
    print("----------------------------------------------------------")
    input("Press enter to start the game")
def end_page(board,players):
    print("The game has ended!")
    print("----------------------------------------------------------")
    winner = max(players, key=lambda player: player.money)
    print(f"{winner.name} has won the game with ${winner.money}!")
    print("Check out more details:")
    for player in players:
        print(f"{player.name} ended the game with ${player.money} and on space {board[player.position].name}")
    print("----------------------------------------------------------")

if __name__ == "__main__":
    
    board,roller = parseArgs()
    welcome_page()

    peter = Player("Green")
    billy = Player("Red")
    charlotte = Player("Yellow")
    sweedal = Player("Blue")
    players = [peter,billy,charlotte,sweedal]

    playerIndex = 0
    totalNumOfCells = len(board.cells)

    while not gameEnd():
        currentPlayer = players[playerIndex%4]
        playerIndex += 1

        nextRoll = roller.getNextRoll()

        timesPassGo = (currentPlayer.position + nextRoll) // totalNumOfCells
        currentPlayer.move(nextRoll, totalNumOfCells)

        print("-------------------------\n" + currentPlayer.name)
        print("Rolled: " + str(nextRoll))
        
        # check whether this player pass GO
        if timesPassGo > 0:
            print(currentPlayer.name, "Passing Go, gain $1")
            currentPlayer.money += timesPassGo
        
        if isinstance(board.cells[currentPlayer.position],Go):
            print("Now at: Go")
        else:
            # step on a property
            thisProperty = board.cells[currentPlayer.position]
            print("Now at: " + thisProperty.name)
            
            if thisProperty.owner == None and currentPlayer.money >= thisProperty.price:
                currentPlayer.purchaseProperty(thisProperty)
                print(currentPlayer.name, "Now successfully purchase the property",thisProperty.name)

            else:
                # this property has owned by the player themselves
                if thisProperty.owner.name == currentPlayer.name:
                    print("This property is already owned by", currentPlayer.name)
                    continue
                else:
                    #this property is own by someone else, check if the whole set owned by same player, if yes double the  price
                    rent = thisProperty.price
                    colourSet = thisProperty.colour
                    propertiesSet = board.properties_Set[colourSet]
                    
                    owners = []
                    for p in propertiesSet:
                        if p.owner is None:
                            break
                        else:
                            owners.append(p.owner)
                    if len(owners) == len(propertiesSet) and all(element == owners[0] for element in owners):
                        print("The whole set is owned by",owners[0].name)
                        rent = rent * 2

                    currentPlayer.payRent(thisProperty.owner,rent)
                    print(currentPlayer.name, "paying", thisProperty.owner.name, thisProperty.price)

    end_page(board.cells,players)