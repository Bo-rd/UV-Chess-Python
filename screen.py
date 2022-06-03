import button
import os
import piece
import tile as Tile
import pygame
import math
import sys
import fpstimer

from player import Player
GAMETILES = []
(WIDTH, HEIGHT) = (800, 800)
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CURTEAM = "White"    # Keeps track of whose turn it is

def getScreen():
    return SCREEN


ROWS = 16
COLS = 16

TILES = [[0 for i in range(COLS)] for j in range(ROWS)]

# creates the chess board

def createBoard():
    global TILES
    for x in range(ROWS):
        for y in range(COLS):
            TILES[y][x] = Tile.Tile(x, y, x % 2 + y % 2)
createBoard()

def getRows():
    return ROWS

def getCols():
    return COLS

mousePos = pygame.mouse.get_pos()

piece_toggle = False
saved_x = None
saved_y = None

def eventHandler():
    global TILES
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
            mouseX, mouseY = mousePos
            tileX = math.floor(mouseX/50)
            tileY = math.floor(mouseY/50)

            print("Checking: " + str(tileX) + ", " + str(tileY))
            print(TILES[tileY][tileX].getHasPiece())

            if TILES[tileY][tileX].getHasPiece() and not piece_toggle:
                toggle_ON_piece_clicked(tileX, tileY)
            elif piece_toggle:
                TILES[saved_y][saved_x].getPiece().setPos(tileX, tileY)
                TILES[tileY][tileX].putPiece(TILES[saved_y][saved_x].getPiece())
                TILES[saved_y][saved_x].removePiece()
                toggle_OFF_piece_clicked()


def getMousePos():
    global mousePos
    return mousePos

def toggle_ON_piece_clicked(savedXPos, savedYPos):
    print("Toggled on")
    global piece_toggle, saved_x, saved_y
    piece_toggle = True
    saved_x = savedXPos
    saved_y = savedYPos

def toggle_OFF_piece_clicked():
    print("Toggled off")
    global piece_toggle, saved_x, saved_y
    piece_toggle = False
    saved_x = None
    saved_y = None

def getToggle():
    global piece_toggle
    return piece_toggle

def getSavedX():
    global piece_toggle, saved_x
    if piece_toggle:
        return saved_x

def getSavedY():
    global piece_toggle, saved_y
    if piece_toggle:
        return saved_y

def getSavedPiece():
    global piece_toggle, saved_x, saved_y, TILES
    if piece_toggle:
        return TILES[saved_y][saved_x].getPiece()


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
        print("Put at: " + str(i.getX()) + ", " + str(i.getY()))


# this should be used to update every frame
def tick():
    global TILES
    eventHandler()
    for x in range(getRows()):
        for y in range(getCols()):
            TILES[y][x].tick()
    bluePlayer.playerTick()
    #redPlayer.playerTick()
    #whitePlayer.playerTick()
    #blackPlayer.playerTick()


# this should be used to draw every frame
def render(screen):
    global TILES
    for x in range(getRows()):
        for y in range(getCols()):
            TILES[y][x].render(SCREEN)
    bluePlayer.playerRender(SCREEN)
    #redPlayer.playerRender(screen)
    #blackPlayer.playerRender(screen)
    #whitePlayer.playerRender(screen)
    pygame.display.flip()


def initBoard():
    createBoard()

def mainloop():
    print("In mainloop...")
    initBoard()
    initPieces()
    fps = fpstimer.FPSTimer(60)
    while True:
        tick()
        render(SCREEN)
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
