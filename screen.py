import button
import os
import piece
import tile
from pickle import TRUE
import pygame
import sys


ROWS = 16
COLS = 16
TILES = [[0 for i in range(COLS)] for j in range(ROWS)]

#App Folder directory
app_folder = os.path.dirname(os.path.realpath(sys.argv[0]))
os.chdir(app_folder)

# pygame initialization and screen generation
pygame.init()
background_colour = (169, 169, 169)
(width, height) = (800, 800)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('UV Chess')
screen.fill(background_colour)
pygame.display.update()
running = True

# creates the chess board
def createBoard(running):
    board_made = False
    while running:
        if board_made is False:
            for x in range(ROWS):
                for y in range(COLS):
                    TILES[y][x] = tile.Tile(x, y, x % 2 + y % 2)
            for x in range(ROWS):
                for y in range(COLS):
                    TILES[y][x].draw(screen)
            board_made = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


def startMenu():
    menuRunning = True
    img_size = (700, 350)
    white = (255, 255, 255)
    startSplash = pygame.image.load(r'./graphics/Logo.png')
    startSplash = pygame.transform.scale(startSplash, img_size)
    start_button = pygame.image.load(r'./graphics/StartButton.png')
    startButton = button.Button(150, 300, start_button)
    while menuRunning:
        screen.fill(white)
        # places splash image on screen
        screen.blit(startSplash, (50, 0))
        if startButton.draw(screen):
            createBoard(running)
            menuRunning = False

        # iterate over the list of Event objects
        # that was returned by pygame.event.get() method.
        for event in pygame.event.get():
            # if event object type is QUIT
            # then quitting the pygame
            # and program both.
            if event.type == pygame.QUIT:
                # deactivates the pygame library
                pygame.quit()
                # quit the program.
                quit()
            # Draws the surface object to the screen.
            pygame.display.update()


startMenu()
pawn = piece.Test(10, 8, None, None, "blue pawn", TILES)
pawn.draw(screen)
