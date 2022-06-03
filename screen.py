import button
import os
import piece
import tile as Tile
import pygame
import sys
import fpstimer
import handler as HANDLER

from player import Player
GAMETILES = []
(WIDTH, HEIGHT) = (800, 800)
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CURTEAM = "White"    # Keeps track of whose turn it is
HANDLER.setScreen(SCREEN)

def getScreen():
    return SCREEN


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
        HANDLER.eventHandler()
        SCREEN.fill(white)
        # places splash image on screen
        SCREEN.blit(startSplash, (50, 0))
        if startButton.getClicked():
            HANDLER.createBoard()
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
    global whitePlayer, blackPlayer, bluePlayer, redPlayer
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


# this should be used to update every frame
def tick():
    HANDLER.eventHandler()
    for x in range(HANDLER.getRows()):
        for y in range(HANDLER.getCols()):
            HANDLER.getTiles()[y][x].tick()
    bluePlayer.playerTick()
    #redPlayer.playerTick()
    #whitePlayer.playerTick()
    #blackPlayer.playerTick()


# this should be used to draw every frame
def render(screen):
    for x in range(HANDLER.getRows()):
        for y in range(HANDLER.getCols()):
            HANDLER.getTiles()[y][x].render(screen)
    bluePlayer.playerRender(screen)
    #redPlayer.playerRender(screen)
    #blackPlayer.playerRender(screen)
    #whitePlayer.playerRender(screen)
    pygame.display.flip()


def initBoard():
    HANDLER.createBoard()

def mainloop():
    print("In mainloop...")
    initBoard()
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
PIECES = initPieces()
mainloop()
