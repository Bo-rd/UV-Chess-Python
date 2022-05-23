import button
import os
import piece
from pickle import TRUE
import pygame
import sys



ROWS = 16
COLS = 16
TILES = [[0 for i in range(COLS)] for j in range(ROWS)]

#App Folder directory
app_folder = os.path.dirname(os.path.realpath(sys.argv[0]))
os.chdir(app_folder)

pygame.init()
background_colour = (169, 169, 169)
(width, height) = (800, 800)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('UV Chess')
screen.fill(background_colour)
pygame.display.update()
running = True


class Tile:
    def __init__(self, xPos, yPos, color):
        self.x = xPos
        self.y = yPos
        self.color = color
        self.size = 50
        # Active is used to check for border or corner tiles
        self.active = True
        print("Made a tile at: " + str(self.x) + ", " + str(self.y))

    def draw(self, screen):
        gray = (169, 169, 169)
        black = (0, 0, 0)
        white = (255, 255, 255)
        blue = (0, 0, 255)
        surface = screen

        # Makes pattern on board
        if self.color == 1:
            pygame.draw.rect(surface, white, pygame.Rect(
                self.x*self.size, self.y*self.size, self.size, self.size))
        else:
            pygame.draw.rect(surface, black, pygame.Rect(
                self.x*self.size, self.y*self.size, self.size, self.size))

        # Makes gray corners and blue outline
        if self.x == 0 or self.y == 0 or self.x == 15 or self.y == 15:
            pygame.draw.rect(surface, blue, pygame.Rect(
                self.x*self.size, self.y*self.size, self.size, self.size))
            self.active = False
        if self.x > 0 and self.x < 4 and self.y > 0 and self.y < 4:
            pygame.draw.rect(surface, gray, pygame.Rect(
                self.x*self.size, self.y*self.size, self.size, self.size))
            self.active = False
        if self.x > 11 and self.x < 15 and self.y > 11 and self.y < 15:
            pygame.draw.rect(surface, gray, pygame.Rect(
                self.x*self.size, self.y*self.size, self.size, self.size))
            self.active = False

        if self.x > 0 and self.x < 4 and self.y > 11 and self.y < 15:
            pygame.draw.rect(surface, gray, pygame.Rect(
                self.x*self.size, self.y*self.size, self.size, self.size))
            self.active = False
        if self.x > 11 and self.x < 15 and self.y > 0 and self.y < 4:
            pygame.draw.rect(surface, gray, pygame.Rect(
                self.x*self.size, self.y*self.size, self.size, self.size))
            self.active = False
        # For some reason this draws to the screen, don't ask why I have no idea yet
        pygame.display.update()

    def getPos(self):
        print(self.x + ", " + self.y)

#creates the chess board
def createBoard(running):
    board_made = False
    while running:
        if board_made is False:
            for x in range(ROWS):
                for y in range(COLS):
                    TILES[y][x] = Tile(x, y, x % 2 + y % 2)
            for x in range(ROWS):
                for y in range(COLS):
                    TILES[y][x].draw(screen)
            board_made = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

def startMenu():
    menuRunning = True
    img_size = (700,350)
    white = (255, 255, 255)
    startSplash = pygame.image.load(r'./graphics/Logo.png')
    startSplash = pygame.transform.scale(startSplash, img_size)
    start_button = pygame.image.load(r'./graphics/StartButton.png')
    startButton = button.Button(150, 300, start_button)
    while menuRunning :
        screen.fill(white)
    
        #places splash image on screen
        screen.blit(startSplash, (50, 0))
        
        if startButton.draw(screen):
            createBoard(running)
            menuRunning = False

    
        # iterate over the list of Event objects
        # that was returned by pygame.event.get() method.
        for event in pygame.event.get() :
    
            # if event object type is QUIT
            # then quitting the pygame
            # and program both.
            if event.type == pygame.QUIT :
    
                # deactivates the pygame library
                pygame.quit()
    
                # quit the program.
                quit()
    
            # Draws the surface object to the screen.  
            pygame.display.update() 

startMenu()
pawn = piece.Test(10, 8, None, None, "blue pawn", TILES)
pawn.draw(screen)