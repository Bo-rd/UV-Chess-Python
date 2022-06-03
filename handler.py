import tile
import pygame

screen = None

ROWS = 16
COLS = 16

TILES = [[0 for i in range(COLS)] for j in range(ROWS)]

# creates the chess board

def createBoard():
    for x in range(ROWS):
        for y in range(COLS):
            TILES[y][x] = tile.Tile(x, y, x % 2 + y % 2)



def getTiles():
    return TILES

def getRows():
    return ROWS

def getCols():
    return COLS

def setScreen(newScreen):
    global screen
    screen = newScreen

mousePos = None


def eventHandler():
    global mousePos
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

#def mouseManager():
#    if pygame.mouse.get_pressed()[0] == 1 and

#            if pygame.mouse.get_pressed()[0] == 0:
        #elif event.type == pygame.MOUSEMOTION:

def getMousePos():
    global mousePos
    return mousePos

piece_toggle = False
clicked_piece = None

def toggle_ON_piece_clicked(self, value, pieceClicked):
    global piece_toggle, clicked_piece
    piece_toggle = True
    clicked_piece = pieceClicked

def toggle_OFF_piece_clicked(self):
    global piece_toggle, piece_held
    piece_toggle = False
    piece_held = None
