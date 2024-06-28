import random
from piece import Piece

class Board:
    def __init__(self, size, prob):
        self.size = size
        self.board = []
        self.won = False 
        self.lost = False
        self.totalMines = 0
        self.remainingMines = 0
        self.flagsUsed = 0

        for row in range(size[0]):
            row = []
            for col in range(size[1]):
                bomb = random.random() < prob
                if bomb:
                    self.totalMines += 1
                piece = Piece(bomb)
                row.append(piece)
            self.board.append(row)
        self.remainingMines = self.totalMines
        self.setNeighbors()
        self.setNumAround()

    def print(self):
        print(f"Mines remaining: {self.remainingMines}")
        for row in self.board:
            for piece in row:
                print('F' if piece.getFlagged() else 'C' if piece.getClicked() else '?', end=' ')
            print()

    def getBoard(self):
        return self.board

    def getSize(self):
        return self.size
    
    def getPiece(self, index):
        return self.board[index[0]][index[1]]

    def handleClick(self, piece, flag):
        if piece.getClicked() or (piece.getFlagged() and not flag):
            return
        if flag:
            if not piece.getFlagged() and self.flagsUsed >= self.totalMines:
                print("No more flags available!")
                return
            piece.toggleFlag()
            if piece.getFlagged():
                if piece.getHasBomb():
                    piece.setFlagCorrect(True)
                    self.remainingMines -= 1
                self.flagsUsed += 1
            else:
                if piece.isFlagCorrect():
                    piece.setFlagCorrect(False)
                    self.remainingMines += 1
                self.flagsUsed -= 1
            self.checkWon()
            return
        piece.handleClick()
        if piece.getNumAround() == 0:
            for neighbor in piece.getNeighbors():
                self.handleClick(neighbor, False)
        if piece.getHasBomb():
            self.lost = True
        else:
            self.checkWon()
    
    def checkWon(self):
        all_cells_discovered = True
        all_flags_correct = True

        for row in self.board:
            for piece in row:
                if not piece.getHasBomb() and not piece.getClicked():
                    all_cells_discovered = False
                if piece.getHasBomb() and not piece.getFlagged():
                    all_flags_correct = False
                if piece.getFlagged() and not piece.getHasBomb():
                    all_flags_correct = False

        if all_cells_discovered or all_flags_correct:
            self.won = True
        else:
            self.won = False

    def checkWonByFlags(self):
        self.won = True

    def getWon(self):
        return self.won

    def getLost(self):
        return self.lost

    def setNeighbors(self):
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                piece = self.board[row][col]
                neighbors = []
                self.addToNeighborsList(neighbors, row, col)
                piece.setNeighbors(neighbors)
    
    def addToNeighborsList(self, neighbors, row, col):
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if r == row and c == col:
                    continue
                if r < 0 or r >= self.size[0] or c < 0 or c >= self.size[1]:
                    continue
                neighbors.append(self.board[r][c])
    
    def setNumAround(self):
        for row in self.board:
            for piece in row:
                piece.setNumAround()
