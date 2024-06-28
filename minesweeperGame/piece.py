class Piece:
    # reprezinta o piesa individuala din joc
    def __init__(self, hasBomb):
        # initializez clasa de piee
        self.hasBomb = hasBomb
        self.around = 0
        self.clicked = False
        self.flagged = False
        self.neighbors = []
        self.correctFlag = False

# indic daca are mina
    def __str__(self):
        return str(self.hasBomb)

# numarul de mine din jurul piesei
    def getNumAround(self):
        return self.around
    
# indic daca are mina
    def getHasBomb(self):
        return self.hasBomb

# indic daca a fost apasata sau nu
    def getClicked(self):
        return self.clicked

# indic daca e marcata cu flag sau nu
    def getFlagged(self):
        return self.flagged

# demarchez daca apas iar pe ea
    def toggleFlag(self):
        self.flagged = not self.flagged

# starea piesei e deschisa
    def handleClick(self):
        self.clicked = True

# calc nr de mine din jurul piesei
    def setNumAround(self):
        num = 0
        for neighbor in self.neighbors:
            if neighbor.getHasBomb():
                num += 1
        self.around = num

# setez lista de vecini
    def setNeighbors(self, neighbors):
        self.neighbors = neighbors
        
    def getNeighbors(self):
        return self.neighbors
# returneaza daca steagul e pus corect
    def isFlagCorrect(self):
        return self.correctFlag
# seteaza daca steagul pus e corect sau nu
    def setFlagCorrect(self, correct):
        self.correctFlag = correct
