import button
import os
import piece
import tile
import pygame
import sys
import fpstimer

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
    pawn = piece.Test(xPos=200, yPos=250, team=None, graphicPath=os.path.join("graphics", "pieces", "blue", "pawnBlue.png"),
                      pieceId="blue pawn", tilesList=TILES, surface=SCREEN)
    pawn.draw()
    return pawn

# this should be used to update every frame
def tick():
    SCREEN.blit(PIECES.graphic, PIECES.rect)

# this should be used to draw every frame
def render(screen):
    pygame.display.flip()


def mainloop():
    print("In mainloop...")
    fps = fpstimer.FPSTimer(60)
    while True:
        tick()
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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print("Mouse down")
                print(PIECES.rect.x)
                print(PIECES.moving)
                if PIECES.rect.collidepoint(event.pos):
                    print("Found piece")
                    PIECES.moving = True
                print(PIECES.moving)
            elif event.type == pygame.MOUSEBUTTONUP:
                print("Mouse Up")
                PIECES.moving = False
            elif event.type == pygame.MOUSEMOTION and PIECES.moving:
                print("Mouse Moving")
                PIECES.move(event)

            pygame.display.update()
        fps.sleep()


"""GAME INIT"""

#App Folder directory
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
