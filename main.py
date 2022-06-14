"""
4 player Chess - Python
Summer 2022
-
Andrew P -- Christopher Wilkinson -- Joshua Kitchen -- Max Diamond -- Seth Bird
-
This is our main driver file. It will be responsible for handling user input and displaying the current GameState object on screen.
"""
import pygame
import ChessEngine
import os
pygame.init() # I read it is wise to initialize pygame right away.
pygame.display.set_caption('UVChess - 4 Player Chess - Summer 2022')
window_icon = pygame.image.load(os.path.join('images', 'window_icon.png'))
pygame.display.set_icon(window_icon)

""" Constants """
WIDTH = 1000
HEIGHT = 1000

NUM_OF_HORIZONTAL_SQUARES = 16
SQUARE_SIZE = HEIGHT // NUM_OF_HORIZONTAL_SQUARES

GAME_PIECE_SCALER = 0.75 # A value 0-1 to scale the game piece to the tile.

MAX_FPS = 60

DARK_TILE_COLOR = pygame.Color(53, 44, 35)
LIGHT_TILE_COLOR = pygame.Color(192, 158, 121)
SMALL_CORNER_COLOR = pygame.Color(89, 89, 89)
LARGE_CORNER_COLOR = pygame.Color(120, 120, 120)
HOVER_COLOR = pygame.Color(252, 186, 3)
SELECTED_COLOR = pygame.Color(3, 157, 252)
WHITE_BORDER_COLOR = pygame.Color(255, 255, 255)
LINE_STROKE_COLOR = pygame.Color(0, 0, 0)
font = pygame.font.Font(None, 25)

# Helps load all the images into memory once. Also makes it easier to swap different piece images without retyping everything (Ex: Wood Piece image files)
IMAGES = {}
def loadImages():
    pieces = ["bR","bN","bB","bQ","bK","bp","wR","wN","wB","wQ","wK","wp","lR","lN","lB","lQ","lK","lp","rR","rN","rB","rQ","rK","rp"]
    for piece in pieces:
        #window_icon = pygame.image.load(os.path.join('images', 'window_icon.png'))
        IMAGES[piece] = pygame.transform.scale(pygame.image.load(os.path.join("images/" + piece + ".png")), (SQUARE_SIZE * GAME_PIECE_SCALER ,SQUARE_SIZE * GAME_PIECE_SCALER))

""" Main Driver for our chess game"""
def main():
    loadImages() # Loads the images so you do not have to keep loading them each time the board is re-drawn.
    hoverTile = (0,0) # Saves the location of the tile that is being hovered for coloring.
    global selectedTile; selectedTile = (0,0) # Holds the location of a selected tile for coloring.
    global sqSelected; sqSelected = () # Holds selected squre from LAST click of the user. (tuple: row, col)
    global playerClicks; playerClicks = [] # Keeps track of player clicks (two tuples: [(6,4), (4,4)])
   
    # The purpose of those six annoying global statements is so we can just call this function to reset the values later on.
    def resetStorageVars():
        global selectedTile; selectedTile = (0,0)
        global sqSelected; sqSelected = ()
        global playerClicks; playerClicks = []        


    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("white"))

    gs = ChessEngine.GameState()

    moveMade = True #Flag for when a move is made
    running = True # Used as the truth value for our while loop

    while running:
        clock.tick(MAX_FPS)
        for gameEvent in pygame.event.get():
            if gameEvent.type == pygame.QUIT:
                running = False

                """ MOUSE HANDLERS """
            # Used to update the hoverTile location that is used to change tile color.
            elif gameEvent.type == pygame.MOUSEMOTION:
                location = pygame.mouse.get_pos()
                col = location[0]//SQUARE_SIZE
                row = location[1]//SQUARE_SIZE
                hoverTile = (row,col)

            # Used when the mouse is clicked.
            elif gameEvent.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos() 
                col = location[0]//SQUARE_SIZE
                row = location[1]//SQUARE_SIZE

                # If the player clicks on the original tile a second time it will deselect.
                if sqSelected == (row, col):
                    resetStorageVars()

                # This is used to make clicking on an empty space "--" for your first click do nothing.
                elif gs.board[row][col] == "--" and len(playerClicks) == 0:
                    resetStorageVars()

                # Prohibits clicking on other player's pieces.
                elif len(playerClicks) == 0 and (gs.board[row][col][0] != ChessEngine.playerList.currentPlayer.colorCode):
                    resetStorageVars()

                # Stores the click into our variables.
                else:                 
                    # This checks if the user clicked in a black corner. If so It will print to console and do nothing waiting for a valid move.
                    if (row <= 3 and col <= 3) or (row >= 12 and col <= 3) or (row <= 3 and col >= 12) or (row >= 12 and col >= 12):
                        print("User clicked on a black corner")

                    # This appends for both the first and second clicks.
                    else:
                        sqSelected = (row, col) 
                        playerClicks.append(sqSelected)

                        selectedTile = sqSelected # For coloring.
                        
                # Second click functionality.
                if len(playerClicks) == 2:
                    selectedMove = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    
                    # If leagal makes the move.
                    if selectedMove in validMoves:
                        print("Rank & File Notation:" + selectedMove.getChessNotation() + "\n") #Prints out the chess notation to the console.
                        gs.makeMove(selectedMove)
                        moveMade = True
                        resetStorageVars()

                    # If illeagal resets.
                    else:
                        print("Illegal Move, try again.")
                        resetStorageVars()


                """ KEY PRESS HANDLERS """
            # Undo functionality when 'z' is pressed the game goes back one move.
            elif gameEvent.type == pygame.KEYDOWN:
                if gameEvent.key == pygame.K_z:
                    gs.undoMove()
                    resetStorageVars()
                    moveMade = True

        # Once a move is made (board has changed). This recalculates the valid moves on the board again.
        if moveMade:
            validMoves = gs.getValidMoves()
            #for i in validMoves: #Uncomment for verbose printing valid moves
            #    print(i.startRow, i.startCol, i.endRow, i.endColumn, i.pieceMoved, i.pieceCaptured, i.moveID)
            moveMade = False

        # Draws the game  
        drawBoard(selectedTile,hoverTile, screen)
        drawPieces(screen, gs.board)
        drawNumAndLetters(screen)
        pygame.display.flip()
    pygame.quit()
    quit()

def drawSquare( color, row, column, screen, stroke = True):
    if stroke:
        pygame.draw.rect(screen, color, pygame.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        pygame.draw.rect(screen, LINE_STROKE_COLOR, pygame.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),2)
    else:
        pygame.draw.rect(screen, color, pygame.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))



""" Displayes the current coloring of the board. The colors can be configured in the constants at the top."""
def drawBoard(selectedTile, hoverTile, screen):
    # Double for loop to go through all the rows and columns.
    for row in range(NUM_OF_HORIZONTAL_SQUARES):
        for column in range(NUM_OF_HORIZONTAL_SQUARES):



            if (row == 0) or (row == 15) or (column == 0) or (column == 15):
                if (row == 0 and column == 0) or (row == 15 and column == 0) or (row == 0 and column == 15) or (row == 15 and column == 15):
                    drawSquare(SMALL_CORNER_COLOR, row, column, screen)
                else:
                    drawSquare(WHITE_BORDER_COLOR, row, column, screen)


            # This code looks for the 3X3 corners and changes them to the SMALL_CORNER_COLOR.
            elif (row <= 3 and column <= 3) or (row >= 12 and column <= 3) or (row <= 3 and column >= 12) or (row >= 12 and column >= 12):
                drawSquare(SMALL_CORNER_COLOR, row, column, screen, False)
                
            # This code makes the cursor easier to see by setting the tile below to the HOVER_COLOR (no hover color when hovering over selected).
            elif(row==hoverTile[0] and column==hoverTile[1]):
                if(row==selectedTile[0] and column==selectedTile[1]):
                    drawSquare(SELECTED_COLOR, row, column, screen)
                else:
                    drawSquare(HOVER_COLOR, row, column, screen)

            # This code changes the color of a selected tile to the SELECTED_COLOR color.
            elif(row==selectedTile[0] and column==selectedTile[1]):
                drawSquare(SELECTED_COLOR, row, column, screen)

            # This code Makes the traditional checkerboard pattern with a LIGHT_TILE_COLOR and a DARK_TILE_COLOR.
            else:
                colors = [LIGHT_TILE_COLOR, DARK_TILE_COLOR] # These three lines could be collapsed but I left it for readability for now.
                color = colors[((row+column) % 2)]
                drawSquare(color, row, column, screen)

            """ This draws the large rectangles in the corners. """
            pygame.draw.rect(screen, LARGE_CORNER_COLOR, pygame.Rect(1 * SQUARE_SIZE, 1 * SQUARE_SIZE, SQUARE_SIZE*3, SQUARE_SIZE*3))
            pygame.draw.rect(screen, LINE_STROKE_COLOR, pygame.Rect(1 * SQUARE_SIZE, 1 * SQUARE_SIZE, SQUARE_SIZE*3, SQUARE_SIZE*3),2)
            pygame.draw.rect(screen, LARGE_CORNER_COLOR, pygame.Rect(12 * SQUARE_SIZE, 1 * SQUARE_SIZE, SQUARE_SIZE*3, SQUARE_SIZE*3))
            pygame.draw.rect(screen, LINE_STROKE_COLOR, pygame.Rect(12 * SQUARE_SIZE, 1 * SQUARE_SIZE, SQUARE_SIZE*3, SQUARE_SIZE*3),2)
            pygame.draw.rect(screen, LARGE_CORNER_COLOR, pygame.Rect(1 * SQUARE_SIZE, 12 * SQUARE_SIZE, SQUARE_SIZE*3, SQUARE_SIZE*3))
            pygame.draw.rect(screen, LINE_STROKE_COLOR, pygame.Rect(1 * SQUARE_SIZE, 12 * SQUARE_SIZE, SQUARE_SIZE*3, SQUARE_SIZE*3),2)       
            pygame.draw.rect(screen, LARGE_CORNER_COLOR, pygame.Rect(12 * SQUARE_SIZE, 12 * SQUARE_SIZE, SQUARE_SIZE*3, SQUARE_SIZE*3))
            pygame.draw.rect(screen, LINE_STROKE_COLOR, pygame.Rect(12 * SQUARE_SIZE, 12 * SQUARE_SIZE, SQUARE_SIZE*3, SQUARE_SIZE*3),2)

def drawPieces(screen, board):
    for row in range(NUM_OF_HORIZONTAL_SQUARES):
        for column in range(NUM_OF_HORIZONTAL_SQUARES):
            piece = board[row][column]
            if piece != "--":
                screen.blit(IMAGES[piece], pygame.Rect((column * SQUARE_SIZE)+(SQUARE_SIZE*(1-GAME_PIECE_SCALER)/2), (row * SQUARE_SIZE)+(SQUARE_SIZE*(1-GAME_PIECE_SCALER)/2), (SQUARE_SIZE), (SQUARE_SIZE)))

def drawNumAndLetters(screen):
    # Top Pannel
    text = font.render("a", True, LINE_STROKE_COLOR)
    text_rect = text.get_rect(center=((3 * SQUARE_SIZE)/2, (1 * SQUARE_SIZE)/2))
    screen.blit(text, text_rect)
    text = font.render("b", True, LINE_STROKE_COLOR)
    text_rect = text.get_rect(center=((5 * SQUARE_SIZE)/2, (1 * SQUARE_SIZE)/2))
    screen.blit(text, text_rect)
    text = font.render("c", True, LINE_STROKE_COLOR)
    text_rect = text.get_rect(center=((7 * SQUARE_SIZE)/2, (1 * SQUARE_SIZE)/2))
    screen.blit(text, text_rect)
    text = font.render("d", True, LINE_STROKE_COLOR)
    text_rect = text.get_rect(center=((9 * SQUARE_SIZE)/2, (1 * SQUARE_SIZE)/2))
    screen.blit(text, text_rect)            
    text = font.render("e", True, LINE_STROKE_COLOR)
    text_rect = text.get_rect(center=((11 * SQUARE_SIZE)/2, (1 * SQUARE_SIZE)/2))
    screen.blit(text, text_rect)
    text = font.render("f", True, LINE_STROKE_COLOR)
    text_rect = text.get_rect(center=((13 * SQUARE_SIZE)/2, (1 * SQUARE_SIZE)/2))
    screen.blit(text, text_rect)
    text = font.render("g", True, LINE_STROKE_COLOR)
    text_rect = text.get_rect(center=((15 * SQUARE_SIZE)/2, (1 * SQUARE_SIZE)/2))
    screen.blit(text, text_rect)
    text = font.render("h", True, LINE_STROKE_COLOR)
    text_rect = text.get_rect(center=((17 * SQUARE_SIZE)/2, (1 * SQUARE_SIZE)/2))
    screen.blit(text, text_rect) 
    text = font.render("i", True, LINE_STROKE_COLOR)
    text_rect = text.get_rect(center=((19 * SQUARE_SIZE)/2, (1 * SQUARE_SIZE)/2))
    screen.blit(text, text_rect)
    text = font.render("j", True, LINE_STROKE_COLOR)
    text_rect = text.get_rect(center=((21 * SQUARE_SIZE)/2, (1 * SQUARE_SIZE)/2))
    screen.blit(text, text_rect)
    text = font.render("k", True, LINE_STROKE_COLOR)
    text_rect = text.get_rect(center=((23 * SQUARE_SIZE)/2, (1 * SQUARE_SIZE)/2))
    screen.blit(text, text_rect)
    text = font.render("l", True, LINE_STROKE_COLOR)
    text_rect = text.get_rect(center=((25 * SQUARE_SIZE)/2, (1 * SQUARE_SIZE)/2))
    screen.blit(text, text_rect)             
    text = font.render("m", True, LINE_STROKE_COLOR)
    text_rect = text.get_rect(center=((27 * SQUARE_SIZE)/2, (1 * SQUARE_SIZE)/2))
    screen.blit(text, text_rect)
    text = font.render("n", True, LINE_STROKE_COLOR)
    text_rect = text.get_rect(center=((29 * SQUARE_SIZE)/2, (1 * SQUARE_SIZE)/2))
    screen.blit(text, text_rect) 

    # Bottom Pannel
    text = font.render("a", True, LINE_STROKE_COLOR)
    text_rect = text.get_rect(center=((3 * SQUARE_SIZE)/2, (31 * SQUARE_SIZE)/2))
    screen.blit(text, text_rect)
    text = font.render("b", True, LINE_STROKE_COLOR)
    text_rect = text.get_rect(center=((5 * SQUARE_SIZE)/2, (31 * SQUARE_SIZE)/2))
    screen.blit(text, text_rect)
    text = font.render("c", True, LINE_STROKE_COLOR)
    text_rect = text.get_rect(center=((7 * SQUARE_SIZE)/2, (31 * SQUARE_SIZE)/2))
    screen.blit(text, text_rect)
    text = font.render("d", True, LINE_STROKE_COLOR)
    text_rect = text.get_rect(center=((9 * SQUARE_SIZE)/2, (31 * SQUARE_SIZE)/2))
    screen.blit(text, text_rect)            
    text = font.render("e", True, LINE_STROKE_COLOR)
    text_rect = text.get_rect(center=((11 * SQUARE_SIZE)/2, (31 * SQUARE_SIZE)/2))
    screen.blit(text, text_rect)
    text = font.render("f", True, LINE_STROKE_COLOR)
    text_rect = text.get_rect(center=((13 * SQUARE_SIZE)/2, (31 * SQUARE_SIZE)/2))
    screen.blit(text, text_rect)
    text = font.render("g", True, LINE_STROKE_COLOR)
    text_rect = text.get_rect(center=((15 * SQUARE_SIZE)/2, (31 * SQUARE_SIZE)/2))
    screen.blit(text, text_rect)
    text = font.render("h", True, LINE_STROKE_COLOR)
    text_rect = text.get_rect(center=((17 * SQUARE_SIZE)/2, (31 * SQUARE_SIZE)/2))
    screen.blit(text, text_rect) 
    text = font.render("i", True, LINE_STROKE_COLOR)
    text_rect = text.get_rect(center=((19 * SQUARE_SIZE)/2, (31 * SQUARE_SIZE)/2))
    screen.blit(text, text_rect)
    text = font.render("j", True, LINE_STROKE_COLOR)
    text_rect = text.get_rect(center=((21 * SQUARE_SIZE)/2, (31 * SQUARE_SIZE)/2))
    screen.blit(text, text_rect)
    text = font.render("k", True, LINE_STROKE_COLOR)
    text_rect = text.get_rect(center=((23 * SQUARE_SIZE)/2, (31 * SQUARE_SIZE)/2))
    screen.blit(text, text_rect)
    text = font.render("l", True, LINE_STROKE_COLOR)
    text_rect = text.get_rect(center=((25 * SQUARE_SIZE)/2, (31 * SQUARE_SIZE)/2))
    screen.blit(text, text_rect)             
    text = font.render("m", True, LINE_STROKE_COLOR)
    text_rect = text.get_rect(center=((27 * SQUARE_SIZE)/2, (31 * SQUARE_SIZE)/2))
    screen.blit(text, text_rect)
    text = font.render("n", True, LINE_STROKE_COLOR)
    text_rect = text.get_rect(center=((29 * SQUARE_SIZE)/2, (31 * SQUARE_SIZE)/2))
    screen.blit(text, text_rect) 

    # Left Pannel
    text = font.render("1", True, LINE_STROKE_COLOR)
    text_rect = text.get_rect(center=((1 * SQUARE_SIZE)/2, (3 * SQUARE_SIZE)/2))
    screen.blit(text, text_rect)
    text = font.render("2", True, LINE_STROKE_COLOR)
    text_rect = text.get_rect(center=((1 * SQUARE_SIZE)/2, (5 * SQUARE_SIZE)/2))
    screen.blit(text, text_rect)
    text = font.render("3", True, LINE_STROKE_COLOR)
    text_rect = text.get_rect(center=((1 * SQUARE_SIZE)/2, (7 * SQUARE_SIZE)/2))
    screen.blit(text, text_rect)
    text = font.render("4", True, LINE_STROKE_COLOR)
    text_rect = text.get_rect(center=((1 * SQUARE_SIZE)/2, (9 * SQUARE_SIZE)/2))
    screen.blit(text, text_rect)            
    text = font.render("5", True, LINE_STROKE_COLOR)
    text_rect = text.get_rect(center=((1 * SQUARE_SIZE)/2, (11 * SQUARE_SIZE)/2))
    screen.blit(text, text_rect)
    text = font.render("6", True, LINE_STROKE_COLOR)
    text_rect = text.get_rect(center=((1 * SQUARE_SIZE)/2, (13 * SQUARE_SIZE)/2))
    screen.blit(text, text_rect)
    text = font.render("7", True, LINE_STROKE_COLOR)
    text_rect = text.get_rect(center=((1 * SQUARE_SIZE)/2, (15 * SQUARE_SIZE)/2))
    screen.blit(text, text_rect)
    text = font.render("8", True, LINE_STROKE_COLOR)
    text_rect = text.get_rect(center=((1 * SQUARE_SIZE)/2, (17 * SQUARE_SIZE)/2))
    screen.blit(text, text_rect) 
    text = font.render("9", True, LINE_STROKE_COLOR)
    text_rect = text.get_rect(center=((1 * SQUARE_SIZE)/2, (19 * SQUARE_SIZE)/2))
    screen.blit(text, text_rect)
    text = font.render("10", True, LINE_STROKE_COLOR)
    text_rect = text.get_rect(center=((1 * SQUARE_SIZE)/2, (21 * SQUARE_SIZE)/2))
    screen.blit(text, text_rect)
    text = font.render("11", True, LINE_STROKE_COLOR)
    text_rect = text.get_rect(center=((1 * SQUARE_SIZE)/2, (23 * SQUARE_SIZE)/2))
    screen.blit(text, text_rect)
    text = font.render("12", True, LINE_STROKE_COLOR)
    text_rect = text.get_rect(center=((1 * SQUARE_SIZE)/2, (25 * SQUARE_SIZE)/2))
    screen.blit(text, text_rect)             
    text = font.render("13", True, LINE_STROKE_COLOR)
    text_rect = text.get_rect(center=((1 * SQUARE_SIZE)/2, (27 * SQUARE_SIZE)/2))
    screen.blit(text, text_rect)
    text = font.render("14", True, LINE_STROKE_COLOR)
    text_rect = text.get_rect(center=((1 * SQUARE_SIZE)/2, (29 * SQUARE_SIZE)/2))
    screen.blit(text, text_rect) 

    # Right Pannel
    text = font.render("1", True, LINE_STROKE_COLOR)
    text_rect = text.get_rect(center=((31 * SQUARE_SIZE)/2, (3 * SQUARE_SIZE)/2))
    screen.blit(text, text_rect)
    text = font.render("2", True, LINE_STROKE_COLOR)
    text_rect = text.get_rect(center=((31 * SQUARE_SIZE)/2, (5 * SQUARE_SIZE)/2))
    screen.blit(text, text_rect)
    text = font.render("3", True, LINE_STROKE_COLOR)
    text_rect = text.get_rect(center=((31 * SQUARE_SIZE)/2, (7 * SQUARE_SIZE)/2))
    screen.blit(text, text_rect)
    text = font.render("4", True, LINE_STROKE_COLOR)
    text_rect = text.get_rect(center=((31 * SQUARE_SIZE)/2, (9 * SQUARE_SIZE)/2))
    screen.blit(text, text_rect)            
    text = font.render("5", True, LINE_STROKE_COLOR)
    text_rect = text.get_rect(center=((31 * SQUARE_SIZE)/2, (11 * SQUARE_SIZE)/2))
    screen.blit(text, text_rect)
    text = font.render("6", True, LINE_STROKE_COLOR)
    text_rect = text.get_rect(center=((31 * SQUARE_SIZE)/2, (13 * SQUARE_SIZE)/2))
    screen.blit(text, text_rect)
    text = font.render("7", True, LINE_STROKE_COLOR)
    text_rect = text.get_rect(center=((31 * SQUARE_SIZE)/2, (15 * SQUARE_SIZE)/2))
    screen.blit(text, text_rect)
    text = font.render("8", True, LINE_STROKE_COLOR)
    text_rect = text.get_rect(center=((31 * SQUARE_SIZE)/2, (17 * SQUARE_SIZE)/2))
    screen.blit(text, text_rect) 
    text = font.render("9", True, LINE_STROKE_COLOR)
    text_rect = text.get_rect(center=((31 * SQUARE_SIZE)/2, (19 * SQUARE_SIZE)/2))
    screen.blit(text, text_rect)
    text = font.render("10", True, LINE_STROKE_COLOR)
    text_rect = text.get_rect(center=((31 * SQUARE_SIZE)/2, (21 * SQUARE_SIZE)/2))
    screen.blit(text, text_rect)
    text = font.render("11", True, LINE_STROKE_COLOR)
    text_rect = text.get_rect(center=((31 * SQUARE_SIZE)/2, (23 * SQUARE_SIZE)/2))
    screen.blit(text, text_rect)
    text = font.render("12", True, LINE_STROKE_COLOR)
    text_rect = text.get_rect(center=((31 * SQUARE_SIZE)/2, (25 * SQUARE_SIZE)/2))
    screen.blit(text, text_rect)             
    text = font.render("13", True, LINE_STROKE_COLOR)
    text_rect = text.get_rect(center=((31 * SQUARE_SIZE)/2, (27 * SQUARE_SIZE)/2))
    screen.blit(text, text_rect)
    text = font.render("14", True, LINE_STROKE_COLOR)
    text_rect = text.get_rect(center=((31 * SQUARE_SIZE)/2, (29 * SQUARE_SIZE)/2))
    screen.blit(text, text_rect)

if __name__ == "__main__":
    main()
