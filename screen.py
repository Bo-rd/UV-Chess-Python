import button
import os
import piece
import tile
import pygame
import sys
import fpstimer

from player import Player

ROWS = 16
COLS = 16
TILES = [[0 for i in range(COLS)] for j in range(ROWS)]
GAMETILES = []
(WIDTH, HEIGHT) = (800, 800)
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
DIRTY_BLITS = []


# creates the chess board
def createBoard():
    print("Drawing tiles...")
    for x in range(ROWS):
        for y in range(COLS):
            TILES[y][x] = tile.Tile(x, y, x % 2 + y % 2)
    for x in range(ROWS):
        for y in range(COLS):
            TILES[y][x].draw(SCREEN)


def startMenu():
    print("Starting...")
    menuRunning = True
    img_size = (700, 350)
    white = (255, 255, 255)
    startSplash = pygame.image.load(r'./graphics/Logo.png')
    startSplash = pygame.transform.scale(startSplash, img_size)
    start_button = pygame.image.load(r'./graphics/StartButton.png')
    startButton = button.Button(150, 300, start_button)
    while menuRunning:
        SCREEN.fill(white)
        # places splash image on screen
        SCREEN.blit(startSplash, (50, 0))
        if startButton.draw(SCREEN):
            createBoard()
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


def initPieces():
    print("Initializing pieces...")
    # pawn = piece.Test(xPos=225, yPos=125, team=None,
    #                   graphicPath=os.path.join("graphics", "pieces", "blue", "pawnBlue.png"),
    #                   pieceId="blue pawn", tilesList=TILES, surface=SCREEN)
    # pawngrn = piece.Test(xPos=125, yPos=225, team=None,
    #                      graphicPath=os.path.join("graphics", "pieces", "black", "pawnBlack.png"),
    #                      pieceId="black pawn", tilesList=TILES, surface=SCREEN)
    # pawn.draw()
    # pawngrn.draw()

    blueStart = [(225, 75), (275, 75), (325, 75), (375, 75),
                (425, 75), (475, 75), (525, 75), (575, 75),
                (225, 125), (275, 125), (325, 125), (375, 125),
                (425, 125), (475, 125), (525, 125), (575, 125)]

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

    bluePlayer = Player("Blue Team", "Blue", blueStart, TILES, SCREEN)
    redPlayer = Player("Red Team", "Red", redStart, TILES, SCREEN)
    blackPlayer = Player("Black Team", "Black", blackStart, TILES, SCREEN)
    whitePlayer= Player("White Team", "White", whiteStart, TILES, SCREEN)

    out = [] # holds the pieces for mouse tracking
    out.extend(bluePlayer.getPieces())
    out.extend(redPlayer.getPieces())
    out.extend(blackPlayer.getPieces())
    out.extend(whitePlayer.getPieces())
    
    return out


# this should be used to update every frame
def tick(movingPiece):
    if movingPiece is not None:
        SCREEN.blit(movingPiece.graphic, movingPiece.rect)


# this should be used to draw every frame
def render(screen):
    pygame.display.flip()


def mainloop():
    movingPiece = None
    print("In mainloop...")
    fps = fpstimer.FPSTimer(60)
    while True:
        tick(movingPiece)
        render(SCREEN)
        for event in pygame.event.get():
            # if event object type is QUIT
            # then quitting the pygame
            # and program both.
            if event.type == pygame.QUIT:
                # deactivates the pygame library
                pygame.quit()
                # quit the program.
                quit()

            # Code for moving pieces
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print("Mouse down")
                for piece in PIECES:
                    # Check if mouse is under the piece we want
                    if piece.rect.collidepoint(event.pos):
                        print("Found piece")
                        piece.moving = True
                        movingPiece = piece
            if movingPiece:
                if event.type == pygame.MOUSEBUTTONUP:
                    print("Mouse Up")
                    if movingPiece:
                        movingPiece.moving = False
                elif event.type == pygame.MOUSEMOTION and movingPiece.moving:
                    print("Mouse Moving")
                    movingPiece.move(event)

            pygame.display.update()
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
