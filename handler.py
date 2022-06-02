import tile

screen = None

ROWS = 16
COLS = 16

TILES = [[0 for i in range(COLS)] for j in range(ROWS)]

# creates the chess board

def createBoard():
    print("Drawing tiles...")
    for x in range(ROWS):
        for y in range(COLS):
            TILES[y][x] = tile.Tile(x, y, x % 2 + y % 2)
    for x in range(ROWS):
        for y in range(COLS):
            TILES[y][x].render(screen)


def getTiles():
    return TILES

def getRows():
    return ROWS

def getCols():
    return COLS

def setScreen(newScreen):
    global screen
    screen = newScreen
