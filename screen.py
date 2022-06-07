import button
import os
from tile import Tile
import pygame
import math
import sys
import fpstimer

from player import Player
GAMETILES = []
(WIDTH, HEIGHT) = (800, 800)
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CURTEAM = "White"
ROWS = 16
COLS = 16
TILES = [[0 for i in range(COLS)] for j in range(ROWS)]

MOUSEPOS = pygame.mouse.get_pos()

PIECE_TOGGLED = False
SAVED_PIECE = None

# Coords that keep track of which tile the toggled piece sits on
saved_x = None
saved_y = None

def createBoard():
    global TILES, ROWS
    for x in range(ROWS):
        for y in range(COLS):
            TILES[y][x] = Tile(x, y, x % 2 + y % 2)

def screenToTile(x, y):
    """Converts screen coordinates to an index in the GAMETILES list"""
    return math.floor(x/50), math.floor(y/50)


def startMenu():
    print("Starting...")
    menuRunning = True
    img_size = (700, 350)
    white = (255, 255, 255)
    startSplash = pygame.image.load(r'./graphics/Logo.png')
    startSplash = pygame.transform.scale(startSplash, img_size)
    start_button = pygame.image.load(r'./graphics/StartButton.png')
    startButton = button.Button(150, 300, start_button)
    fps = fpstimer.FPSTimer(60)
    while menuRunning:
        eventHandler()
        SCREEN.fill(white)
        # places splash image on screen
        SCREEN.blit(startSplash, (50, 0))
        if startButton.getClicked():
            createBoard()
            print("Button Pressed")
            menuRunning = False
        startButton.buttonTick()
        startButton.buttonRender(SCREEN)
        pygame.display.flip()
        fps.sleep()


bluePlayer = None
redPlayer = None
whitePlayer = None
blackPlayer = None


def initPieces():
    global whitePlayer, blackPlayer, bluePlayer, redPlayer, TILES
    print("Initializing pieces...")
    """
    start coordinates =
    [rook, bishop, knight, queen, king, ... , pawn1, pawn2, ...]
    Same order in the constructor of Player

    We'll probably want to move the player generation into the
    global scope, or return them as part of a list for access.
    """
    blueStart = [(4, 1), (5, 1), (6, 1), (7, 1),
                (8, 1), (9, 1), (10, 1), (11, 1),
                (4, 2), (5, 2), (6, 2), (7, 2),
                (8, 2), (9, 2), (10, 2), (11, 2)]

    redStart = [(225, 725), (275, 725), (325, 725), (375, 725),
                (425, 725), (475, 725), (525, 725), (575, 725),
                (225, 675), (275, 675), (325, 675), (375, 675),
                (425, 675), (475, 675), (525, 675), (575, 675)]

    blackStart = [(75, 225), (75, 275), (75, 325), (75, 375),
                (75, 425), (75, 475), (75, 525), (75, 575),
                (125, 225), (125, 275), (125, 325), (125, 375),
                (125, 425), (125, 475), (125, 525), (125, 575)]

    whiteStart = [(725, 225), (725, 275), (725, 325), (725, 375),
                (725, 425), (725, 475), (725, 525), (725, 575),
                (675, 225), (675, 275), (675, 325), (675, 375),
                (675, 425), (675, 475), (675, 525), (675, 575)]
    bluePlayer = Player("Blue Team", "Blue", blueStart, SCREEN)
    #redPlayer = Player("Red Team", "Red", redStart, SCREEN)
    #blackPlayer = Player("Black Team", "Black", blackStart, SCREEN)
    #whitePlayer= Player("White Team", "White", whiteStart, SCREEN)

    for i in bluePlayer.getPieces():
        TILES[i.getY()][i.getX()].putPiece(i)
        i.tile = TILES[i.getY()][i.getX()]
        print("Put at: " + str(i.getX()) + ", " + str(i.getY()))

def eventHandler():
    global TILES, SAVED_PIECE, PIECE_TOGGLED
    mousePos = pygame.mouse.get_pos()
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
        elif event.type == pygame.MOUSEBUTTONUP:
            tileX, tileY = screenToTile(mousePos[0], mousePos[1])
            current_tile = TILES[tileY][tileX]
            current_tile.getHasPiece()

            print("Checking: " + str(tileX) + ", " + str(tileY))
            print(TILES[tileY][tileX].getHasPiece())

            if TILES[tileY][tileX].getHasPiece() and not PIECE_TOGGLED:
                PIECE_TOGGLED = True
                SAVED_PIECE = current_tile.getPiece()
                current_tile.clicked = True
                print("Toggled on")

            elif PIECE_TOGGLED:
                SAVED_PIECE.tile.removePiece()
                SAVED_PIECE.tile.clicked = False
                SAVED_PIECE.setPos(tileX, tileY)
                SAVED_PIECE.tile = current_tile
                current_tile.putPiece(SAVED_PIECE)
                PIECE_TOGGLED = False
                print("Toggled off")


# this should be used to update every frame
def tick():
    global TILES, ROWS, COLS
    eventHandler()
    for x in range(ROWS):
        for y in range(COLS):
            TILES[y][x].tick()
    bluePlayer.playerTick()
    #redPlayer.playerTick()
    #whitePlayer.playerTick()
    #blackPlayer.playerTick()


# this should be used to draw every frame
def render():
    global TILES, ROWS, COLS, SCREEN
    for x in range(ROWS):
        for y in range(COLS):
            TILES[y][x].render(SCREEN)
    bluePlayer.playerRender(SCREEN)
    #redPlayer.playerRender(screen)
    #blackPlayer.playerRender(screen)
    #whitePlayer.playerRender(screen)
    pygame.display.flip()

def mainloop():
    print("In mainloop...")
    createBoard()
    initPieces()
    fps = fpstimer.FPSTimer(60)
    while True:
        tick()
        render()
        fps.sleep()


"""GAME INIT"""

# App Folder directory
app_folder = os.path.dirname(os.path.realpath(sys.argv[0]))
os.chdir(app_folder)

# pygame initialization and screen generation
pygame.init()
background_colour = (169, 169, 169)
pygame.display.set_caption('UV Chess')
SCREEN.fill(background_colour)
pygame.display.update()

startMenu()
mainloop()
