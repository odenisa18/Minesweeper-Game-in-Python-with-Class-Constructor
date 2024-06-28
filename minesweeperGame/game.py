import pygame
from piece import Piece 
from board import Board 
import os
from solver import Solver
from time import sleep

class Game:

    # construiesc clasa 
    def __init__(self, size, prob):
    # initializez jocul cu o tabla de joc de dim/ prob specifice
        self.board = Board(size, prob)
        pygame.init()
        self.sizeScreen = 800, 800
        self.textHeight = 50  #  inaltimea textului
        self.screen = pygame.display.set_mode(self.sizeScreen)
        # dimensiunea fiecarei piese pe tabla
        self.pieceSize = (self.sizeScreen[0] / size[1], (self.sizeScreen[1] - self.textHeight) / size[0]) 
        # incarca imaginile pieselor
        self.loadPictures()
        self.solver = Solver(self.board)
        # incarc imag de fundal
        self.load_background_image()
        self.startTime = pygame.time.get_ticks()  # Inițializarea timerului

# incarc imaginile din "casute" in joc 0,1,2,M,etc
    def loadPictures(self):
        self.images = {}
        imagesDirectory = "images"
        for fileName in os.listdir(imagesDirectory):
            if not fileName.endswith(".png"):
                continue
            path = os.path.join(imagesDirectory, fileName)
            img = pygame.image.load(path)
            img = img.convert()
            img = pygame.transform.scale(img, (int(self.pieceSize[0]), int(self.pieceSize[1])))
            self.images[fileName.split(".")[0]] = img

# adaug imaginea de fundal pt fereastra din final
    def load_background_image(self):
        self.background_image = pygame.image.load("path_to_main_background_image.jpg").convert()
        self.background_image = pygame.transform.scale(self.background_image, self.sizeScreen)

# rulez jocul in sine
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return "quit"
                if event.type == pygame.MOUSEBUTTONDOWN and not (self.board.getWon() or self.board.getLost()):
                   # gestionez clickul de pe mouse
                    rightClick = pygame.mouse.get_pressed(num_buttons=3)[2]
                    self.handleClick(pygame.mouse.get_pos(), rightClick)
              # apelez solver pt o mutare
                if event.type == pygame.KEYDOWN:
                    self.solver.move()
            self.screen.fill((0, 0, 0))
            self.draw()
            # actualizez ecranul
            pygame.display.flip()
            # afisez mesajele corespunzatoare win/lose
            if self.board.getWon():
                self.win()
                return "won"
            elif self.board.getLost():
                self.lose()
                return "lost"
            
        pygame.quit()
        return "quit"

    def draw(self):
       # afisez nr de mine ramase in partea de sus a ferestrei
        font = pygame.font.SysFont(None, 35)
        mines_left_text = font.render(f"Mines remaining: {self.board.remainingMines}", True, (255, 255, 255))
        self.screen.blit(mines_left_text, (10, 10))

        # afisez timer-ul
        elapsed_time = (pygame.time.get_ticks() - self.startTime) // 1000
        timer_text = font.render(f"Time: {elapsed_time} s", True, (255, 255, 255))
        self.screen.blit(timer_text, (self.sizeScreen[0] - 150, 10))

        # desenez tabla de joc
        topLeft = (0, self.textHeight)  
        for row in self.board.getBoard():
            for piece in row:
                rect = pygame.Rect(topLeft, self.pieceSize)
                image = self.images[self.getImageString(piece)]
                self.screen.blit(image, topLeft) 
                topLeft = topLeft[0] + self.pieceSize[0], topLeft[1]
            topLeft = (0, topLeft[1] + self.pieceSize[1])

# afisez pe caseta apasata ce se afla acolo 0,1,2,flag etc
    def getImageString(self, piece):
        if piece.getClicked():
            return str(piece.getNumAround()) if not piece.getHasBomb() else 'bomb-at-clicked-block'
        if self.board.getLost():
            if piece.getHasBomb():
                return 'unclicked-bomb'
            return 'wrong-flag' if piece.getFlagged() else 'empty-block'
        return 'flag' if piece.getFlagged() else 'empty-block'

# gestioneaza clickurile pe tabla mea de joc ce inseamna fiecare
    def handleClick(self, position, flag):
        adjusted_position = (position[0], position[1] - self.textHeight)
        index = tuple(int(pos // size) for pos, size in zip(adjusted_position, self.pieceSize))[::-1]
        if 0 <= index[0] < self.board.getSize()[0] and 0 <= index[1] < self.board.getSize()[1]:
            piece = self.board.getPiece(index)
            if flag and not piece.getFlagged() and self.board.flagsUsed >= self.board.totalMines:
                print("No more flags available!")
                return
            self.board.handleClick(piece, flag)

# afisez win si audio
    def win(self):
        sound = pygame.mixer.Sound('win.wav')
        sound.play()
        pygame.time.wait(2000)
        self.show_message("Congratulations! You won!")
# afisez lose si audio
    def lose(self):
        sound = pygame.mixer.Sound('lose.wav')
        sound.play()
        pygame.time.wait(2000)
        self.show_message("Sorry! You lost!")

# functie pentru afisarea mesajelor de mai sus
    def show_message(self, message):
        font = pygame.font.SysFont(None, 75)
        self.screen.fill((0, 0, 0))
        text_surface = font.render(message, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.sizeScreen[0]/2, self.sizeScreen[1]/2))
        self.screen.blit(text_surface, text_rect)
        pygame.display.flip()
        sleep(2)
# afisez meniul de la finalul jocului
    def show_end_menu(self):
        font = pygame.font.SysFont(None, 50)
        options = ["Play Again", "Return to Main Menu", "Quit"]
        selected_option = 0

        while True:
            self.screen.blit(self.background_image, (0, 0))
            for i, option in enumerate(options):
                color = (255, 255, 255) if i == selected_option else (100, 100, 100)
                text_surface = font.render(option, True, color)
                text_rect = text_surface.get_rect(center=(self.sizeScreen[0]/2, self.sizeScreen[1]/2 + i * 60))
                self.screen.blit(text_surface, text_rect)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return "quit"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        selected_option = (selected_option + 1) % len(options)
                    elif event.key == pygame.K_UP:
                        selected_option = (selected_option - 1) % len(options)
                    elif event.key == pygame.K_RETURN:
                        if options[selected_option] == "Play Again":
                            return "play_again"
                        elif options[selected_option] == "Return to Main Menu":
                            return "main_menu"
                        elif options[selected_option] == "Quit":
                            pygame.quit()
                            return "quit"
