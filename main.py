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
pygame.display.set_caption('4 Player Chess - Summer 2022')
window_icon = pygame.image.load(os.path.join('images', 'window_icon.png'))
pygame.display.set_icon(window_icon)

""" Constants """
WIDTH = 1000
HEIGHT = 1000

NUM_OF_HORIZONTAL_SQUARES = 14
SQUARE_SIZE = HEIGHT // NUM_OF_HORIZONTAL_SQUARES

TILE_SCALER = 1 # This is not yet properly implemented but I figured if we wanted to shrink the pieces we could use this. (Changing the number now shrinks but to the corner not center)

MAX_FPS = 60

DARK_TILE_COLOR = pygame.Color("gray")
LIGHT_TILE_COLOR = pygame.Color("white")
BLACKED_OUT_CORNER_COLOR = pygame.Color("black")
HOVER_COLOR = pygame.Color("green")
SELECTED_COLOR = pygame.Color("orange")

# Helps load all the images into memory once. Also makes it easier to swap different piece images without retyping everything (Ex: Wood Piece image files)
IMAGES = {}
def loadImages():
    pieces = ["bR","bN","bB","bQ","bK","bp","wR","wN","wB","wQ","wK","wp","lR","lN","lB","lQ","lK","lp","rR","rN","rB","rQ","rK","rp"]
    for piece in pieces:
        #window_icon = pygame.image.load(os.path.join('images', 'window_icon.png'))
        IMAGES[piece] = pygame.transform.scale(pygame.image.load(os.path.join("images/" + piece + ".png")), (SQUARE_SIZE *TILE_SCALER ,SQUARE_SIZE * TILE_SCALER))

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
                    if (row <= 2 and col <= 2) or (row >= 11 and col <= 2) or (row <= 2 and col >= 11) or (row >= 11 and col >= 11):
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
        pygame.display.flip()
    pygame.quit()
    quit()


""" Displayes the current coloring of the board. The colors can be configured in the constants at the top."""
def drawBoard(selectedTile, hoverTile, screen):
    # Double for loop to go through all the rows and columns.
    for row in range(NUM_OF_HORIZONTAL_SQUARES):
        for column in range(NUM_OF_HORIZONTAL_SQUARES):

            # This code looks for the 3X3 corners and changes them to the BLACKED_OUT_CORNER_COLOR.
            if (row <= 2 and column <= 2) or (row >= 11 and column <= 2) or (row <= 2 and column >= 11) or (row >= 11 and column >= 11):
                pygame.draw.rect(screen, BLACKED_OUT_CORNER_COLOR, pygame.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                
            # This code makes the cursor easier to see by setting the tile below to the HOVER_COLOR (no hover color when hovering over selected).
            elif(row==hoverTile[0] and column==hoverTile[1]):
                if(row==selectedTile[0] and column==selectedTile[1]):
                    pygame.draw.rect(screen, SELECTED_COLOR, pygame.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                else:
                    pygame.draw.rect(screen, HOVER_COLOR, pygame.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

            # This code changes the color of a selected tile to the SELECTED_COLOR color.
            elif(row==selectedTile[0] and column==selectedTile[1]):
                pygame.draw.rect(screen, SELECTED_COLOR, pygame.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

            # This code Makes the traditional checkerboard pattern with a LIGHT_TILE_COLOR and a DARK_TILE_COLOR.
            else:
                colors = [LIGHT_TILE_COLOR, DARK_TILE_COLOR] # These three lines could be collapsed but I left it for readability for now.
                color = colors[((row+column) % 2)]
                pygame.draw.rect(screen, color, pygame.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def drawPieces(screen, board):
    for row in range(NUM_OF_HORIZONTAL_SQUARES):
        for column in range(NUM_OF_HORIZONTAL_SQUARES):
            piece = board[row][column]
            if piece != "--":
                screen.blit(IMAGES[piece], pygame.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

if __name__ == "__main__":
    main()
