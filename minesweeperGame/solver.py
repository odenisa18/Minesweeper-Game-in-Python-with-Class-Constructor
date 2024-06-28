import pyautogui
# constructor de clasa solver
class Solver:
    # rezolvator pt joc
    def __init__(self, board):
        self.board = board

# efect o mutare analizand fiecare piesa de pe tabla de joc
    def move(self):
        # pt fiecare rand
        for row in self.board.getBoard():
            # pt fiecare piesa 
            for piece in row:
                # verific daca a fost deschisa
                if not piece.getClicked():
                    continue
                # obtin nr de mine din jur
                around = piece.getNumAround()
                unknown = 0
                flagged = 0
                # obtin vecinii
                neighbors = piece.getNeighbors()
                for p in neighbors:
                    # pt fiecare vecin
                    # initializeaza contorii pentru piesele necunoscute (unknown) si pentru piesele marcate (flagged).
                    if not p.getClicked():
                        unknown += 1
                    if p.getFlagged():
                        flagged += 1
                if around == flagged:
                    self.openUnflagged(neighbors)
                if around == unknown:
                    self.flagAll(neighbors)

# dechide toate piesele nemarcate dintre vecinii specificati
    def openUnflagged(self, neighbors):
        for piece in neighbors:
            if not piece.getFlagged():
                self.board.handleClick(piece, False)

# marcheaza toate piesele nemarcate dintre vecinii specificati ca avand mine
    def flagAll(self, neighbors):
        for piece in neighbors:
            if not piece.getFlagged():
                self.board.handleClick(piece, True)