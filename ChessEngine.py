"""
4 player Chess - Python
Summer 2022
-
Andrew P -- Christopher Wilkinson -- Joshua Kitchen -- Max Diamond -- Seth Bird
-
#GameState
#Move Log
#Calculate Valid Moves
"""

""" The Node type object that holds player's info for our doubly linked list """
import copy

class ChessPlayerObject:
    def __init__(self, name, gameColor, colorCode, number, nextPlayer = None, previousPlayer = None) -> None:
       self.name = name
       self.gameColor = gameColor
       self.colorCode = colorCode
       self.number = number
       self.nextPlayer = nextPlayer
       self.previousPlayer = previousPlayer

""" Our doubly linked list """
class GamePlayers:
    def __init__(self) -> None:
       self.currentPlayer = None
    
    def nextPlayer(self):
        self.currentPlayer = self.currentPlayer.nextPlayer

    def previousPlayer(self):
        self.currentPlayer = self.currentPlayer.previousPlayer

    # When a player is out of the game they should be removed. This removes them from the doubly linked list.
    def removePlayer(self):
        self.nextPlayer()
        self.currentPlayer.previousPlayer = self.currentPlayer.previousPlayer.previousPlayer

""" Implementing/initiating the player list """
userPlayerNames = ["Alpha", "Bravo", "Charlie", "Delta"] # If we want to implement user submitted usernames in the future we could add them to a list like this

# This creates a linked list to keep the player's info and to make switching easier.
playerList = GamePlayers()
whitePlayer = ChessPlayerObject(userPlayerNames[0], "White", "w", 0, nextPlayer = None, previousPlayer = None)
redPlayer = ChessPlayerObject(userPlayerNames[1], "Red", "r", 1, nextPlayer = None, previousPlayer = whitePlayer)
blackPlayer = ChessPlayerObject(userPlayerNames[2], "Black", "b", 2, nextPlayer = None, previousPlayer = redPlayer)
bluePlayer = ChessPlayerObject(userPlayerNames[3], "Blue", "l", 3, nextPlayer = None, previousPlayer = blackPlayer)

# Since some objects are not created until after these needed to be manually put in.
whitePlayer.nextPlayer = redPlayer
redPlayer.nextPlayer = blackPlayer
blackPlayer.nextPlayer = bluePlayer
bluePlayer.nextPlayer = whitePlayer
whitePlayer.previousPlayer = bluePlayer

# This starts off the doubly linked list with the starting player.
playerList.currentPlayer = whitePlayer

class GameState:
    def __init__(self) -> None:
        # w = White, l = Blue, b = Black, r = Red
        # R = Rook, N = Knight, B = Bishop, Q = Queen, K = King, p = Pawn
        # -- denotes an empty square
        self.board = [
            ["--","--","--","--","--","--","--","--","--","--","--","--","--","--","--","--"],
            ["--","--","--","--","bR","bN","bB","bQ","bK","bB","bN","bR","--","--","--","--"],
            ["--","--","--","--","--","bp","bp","bp","--","bp","bp","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--","--","--","--","--","--","--","--","--"],
            ["--","rR","--","--","--","--","--","--","--","--","--","--","--","--","lR","--"],
            ["--","rN","rp","--","--","--","--","--","--","--","--","--","--","lp","lN","--"],
            ["--","rB","rp","--","--","--","--","--","--","--","--","--","--","lp","lB","--"],
            ["--","rK","--","--","--","--","--","--","--","--","--","--","--","lp","lQ","--"],
            ["--","rQ","rp","--","--","--","--","--","--","--","--","--","--","--","lK","--"],
            ["--","rB","rp","--","--","--","--","--","--","--","--","--","--","lp","lB","--"],
            ["--","rN","rp","--","--","--","--","--","--","--","--","--","--","lp","lN","--"],
            ["--","rR","--","--","--","--","--","--","--","--","--","--","--","--","lR","--"],
            ["--","--","--","--","--","--","--","--","--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","wp","wp","--","wp","wp","wp","--","--","--","--","--"],
            ["--","--","--","--","wR","wN","wB","wK","wQ","wB","wN","wR","--","--","--","--"],
            ["--","--","--","--","--","--","--","--","--","--","--","--","--","--","--","--"]
        ]

        self.whiteKingLocation = (14, 8)
        self.redKingLocation = (8, 1)
        self.blackKingLocation = (1, 8)
        self.blueKingLocation = (8, 14)

        self.moveFunctions = {'p': self.getPawnMoves, "R": self.getRookMoves, "N": self.getKnightMoves, "B": self.getBishopMoves, "Q": self.getQueenMoves, "K": self.getKingMoves}
        self.currentPlayerPrintout = {0:"It is White's Turn", 1:"It is Red's Turn", 2:"It is Black's Turn", 3:"It is Blue's Turn"}
        print(self.currentPlayerPrintout[playerList.currentPlayer.number]) # Prints out initial starting player
        self.moveLog = []
        # Print player name change on change

        """FOR CASTLING"""
        # white
        self.wR_west_moved = False
        self.wR_east_moved = False
        self.wK_moved = False
        # black
        self.bR_west_moved = False
        self.bR_east_moved = False
        self.bK_moved = False
        # blue
        self.lR_north_moved = False
        self.lR_south_moved = False
        self.lK_moved = False
        # red
        self.rR_north_moved = False
        self.rR_south_moved = False
        self.rK_moved = False

    def updateKing(self, move):
        # Updates the King's Position tuple if needed.
        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.endRow, move.endColumn)
        if move.pieceMoved == "rK":
            self.redKingLocation = (move.endRow, move.endColumn)
        if move.pieceMoved == "bK":
            self.blackKingLocation = (move.endRow, move.endColumn)
        if move.pieceMoved == "lK":
            self.blueKingLocation = (move.endRow, move.endColumn)

    """ Moves a chess piece """
    def makeMove(self, move):

        """FOR CASTLING"""
        if move.pieceMoved[1] == "R":
            if move.pieceMoved[0] == "w":
                if move.startCol == 4:
                    if self.wR_west_moved is False:
                        self.wR_west_moved = True
                        print("WHITE WEST ROOK MOVED")
                else:
                    if self.wR_east_moved is False:
                        self.wR_east_moved = True
                        print("WHITE EAST ROOK MOVED")

            elif move.pieceMoved[0] == "b":
                if move.startCol == 4:
                    if self.bR_west_moved is False:
                        self.bR_west_moved = True
                        print("BLACK WEST ROOK MOVED")
                else:
                    if self.bR_east_moved is False:
                        self.bR_east_moved = True
                        print("BLACK EAST ROOK MOVED")

            elif move.pieceMoved[0] == "l":
                if move.startRow == 4:
                    if self.lR_north_moved is False:
                        self.lR_north_moved = True
                        print("BLUE NORTH ROOK MOVED")
                else:
                    if self.lR_south_moved is False:
                        self.lR_south_moved = True
                        print("BLUE SOUTH ROOK MOVED")
            elif move.pieceMoved[0] == "r":
                if move.startRow == 4:
                    if self.rR_north_moved is False:
                        self.rR_north_moved = True
                        print("RED NORTH ROOK MOVED")
                else:
                    if self.rR_south_moved is False:
                        self.rR_south_moved = True
                        print("RED SOUTH ROOK MOVED")
        elif move.pieceMoved[1] == "K":
            if move.pieceMoved[0] == "w":
                if self.wK_moved is False:
                    self.wK_moved = True
                    print("WHITE KING MOVED")
            elif move.pieceMoved[0] == "b":
                if self.bK_moved is False:
                    self.bK_moved = True
                    print("BLACK KING MOVED")
            elif move.pieceMoved[0] == "l":
                if self.lK_moved is False:
                    self.lK_moved = True
                    print("BLUE KING MOVED")
            elif move.pieceMoved[0] == "r":
                if self.rK_moved is False:
                    self.rK_moved = True
                    print("RED KING MOVED")


        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endColumn] = move.pieceMoved
        self.moveLog.append(move) #logs the move
        
        self.updateKing(move) # Checks and Updates the King's Position tuple if needed.

        playerList.nextPlayer()

        print(self.currentPlayerPrintout[playerList.currentPlayer.number]) # Prints new players turn
    

    """ Undoes the last move """
    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endColumn] = move.pieceCaptured

            self.updateKing(move) # Checks and Updates the King's Position tuple if needed.

            playerList.previousPlayer()
            
            print(self.currentPlayerPrintout[playerList.currentPlayer.number]) # Prints new players turn

    # Helper function for getValidMoves. Does same thing as makeMove() but does not change player and log and stuff.

    def getValidMovesHelper(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endColumn] = move.pieceMoved
        self.updateKing(move)



    """All moves considering checks"""
    def getValidMoves(self):
        validMoves = [] # To return valid moves.
        attackerMoveList = [] # To hold potential attacker moves.
        
        boardBackup = copy.deepcopy(self.board) #Copy of the current game board.
        
        # Holds the original king location to restore after checking for checks
        temp1 = self.whiteKingLocation 
        temp2 = self.redKingLocation
        temp3 = self.blackKingLocation
        temp4 = self.blueKingLocation 

        moves = self.getAllPossibleMoves() # Generates the move list for the player like normal.      
    
        for i in range(len(moves)-1,-1,-1): # Goes through that list backwards.
            attackerMoveList = []
            self.getValidMovesHelper(moves[i]) # Moves one piece per loop of the origin color.

            # Adds the next three player's moves into the attackerMoveList list.
            playerList.nextPlayer() 
            attackerMoveList += self.getAllPossibleMoves()
            playerList.nextPlayer() 
            attackerMoveList += self.getAllPossibleMoves()
            playerList.nextPlayer() 
            attackerMoveList += self.getAllPossibleMoves()
            playerList.nextPlayer() #The fourth one just returns back to the right player order.

            testFlag = True
            # Loops through potential other player's moves
            for attackerMove in attackerMoveList:                
                if self.inCheck(attackerMove.endRow, attackerMove.endColumn): # If an other piece puts you into check....
                    testFlag = False
                if testFlag == False:
                    break
            if testFlag == True:
                validMoves.append(moves[i])
            self.board = copy.deepcopy(boardBackup) # Restores the board.
        self.board = copy.deepcopy(boardBackup) # Restores the board.
        # Restores the original king locations
        self.whiteKingLocation  = temp1
        self.redKingLocation = temp2
        self.blackKingLocation = temp3
        self.blueKingLocation  = temp4
        return validMoves 

    """ Determines if the current player is in check """
    def inCheck(self, row, column):
        if playerList.currentPlayer.number == 0:
            return (row == self.whiteKingLocation[0]) and (column == self.whiteKingLocation[1])
        
        if playerList.currentPlayer.number == 1:
            return (row == self.redKingLocation[0]) and (column == self.redKingLocation[1])   

        if playerList.currentPlayer.number == 2:
            return (row == self.blackKingLocation[0]) and (column == self.blackKingLocation[1])

        if playerList.currentPlayer.number == 3:
            return (row == self.blueKingLocation[0]) and (column == self.blueKingLocation[1])


    """All moves without consideriding checks"""
    def getAllPossibleMoves(self):
        moves = []
        for row in range(len(self.board)): 
            for column in range(len(self.board[row])):
                # This calculates moves only for the current players pieces.
                turn = self.board[row][column][0] # Index 0 is the color/player position on the board.
                if (turn == 'w' and playerList.currentPlayer.number == 0) or (turn == 'r' and playerList.currentPlayer.number == 1) or (turn == 'b' and playerList.currentPlayer.number == 2) or (turn == 'l' and playerList.currentPlayer.number == 3):
                    piece = self.board[row][column][1] # Index 1 is the piece type.
                    self.moveFunctions[piece](row, column, moves) # Calls move function for specific piece
        return moves

    # Returnes True if coords are in the 14X14 board AND not in one of those corner spots.
    def isInsideGameGrid(self, endRow, endColumn):
        if 1 <= endRow <= 14 and 1 <= endColumn <= 14 and not ((endRow <= 3 and endColumn <= 3) or (endRow >= 12 and endColumn <= 3) or (endRow <= 3 and endColumn >= 12) or (endRow >= 12 and endColumn >= 12)):
            return True
        return False
    """
    Get all the pawn moves for the pawn located at row, col and add these moves to the list
    """
    def getPawnMoves(self, row, column, moves):

        """ Player 0 is white. This logic is for WHITE Pawns. """
        if playerList.currentPlayer.number == 0: 
            if self.board[row-1][column] == "--":
                moves.append(Move((row, column), (row-1, column), self.board))
                if row == 13 and self.board[row-2][column] == "--":
                    moves.append(Move((row, column), (row-2, column), self.board))
            #Captures to the left
            if column-1 >=1: #Bounds checking
                if (self.board[row-1][column-1][0] != '-') and (self.board[row-1][column-1][0] != 'w'): #Make sure not capturing self or empty
                    moves.append(Move((row, column), (row-1, column-1), self.board))
            #Captures to the right
            if column+1 <=14: #Bounds checking
                if (self.board[row-1][column+1][0] != '-') and (self.board[row-1][column+1][0] != 'w'): #Make sure not capturing self or empty
                    moves.append(Move((row, column), (row-1, column+1), self.board))

        """ Player 1 is red. This logic is for RED Pawns. """
        if playerList.currentPlayer.number == 1: 
            if self.board[row][column+1] == "--":
                moves.append(Move((row, column), (row, column+1), self.board))
                if column == 2 and self.board[row][column+2] == "--":
                    moves.append(Move((row, column), (row, column+2), self.board))
            #Captures upward
            if row-1 >=1: #Bounds checking
                if (self.board[row-1][column+1][0] != '-') and (self.board[row-1][column+1][0] != 'r'): #Make sure not capturing self or empty
                    moves.append(Move((row, column), (row-1, column+1), self.board))
            #Captures downward 
            if row+1 <=14: #Bounds checking
                if (self.board[row+1][column+1][0] != '-') and (self.board[row+1][column+1][0] != 'r'): #Make sure not capturing self or empty
                    moves.append(Move((row, column), (row+1, column+1), self.board))

        """ Player 2 is black. This logic is for BLACK Pawns. """
        if playerList.currentPlayer.number == 2: 
            if self.board[row+1][column] == "--":
                moves.append(Move((row, column), (row+1, column), self.board))
                if row == 2 and self.board[row+2][column] == "--":
                    moves.append(Move((row, column), (row+2, column), self.board))
            #Captures to the left
            if column-1 >=1: #Bounds checking
                if (self.board[row+1][column-1][0] != '-') and (self.board[row+1][column-1][0] != 'b'): #Make sure not capturing self or empty
                    moves.append(Move((row, column), (row+1, column-1), self.board))
            #Captures to the right
            if column+1 <=14: #Bounds checking
                if (self.board[row+1][column+1][0] != '-') and (self.board[row+1][column+1][0] != 'b'): #Make sure not capturing self or empty
                    moves.append(Move((row, column), (row+1, column+1), self.board))

        """ Player 3 is blue. This logic is for BLUE Pawns. """
        if playerList.currentPlayer.number == 3: 
            if self.board[row][column-1] == "--":
                moves.append(Move((row, column), (row, column-1), self.board))
                if column == 13 and self.board[row][column-2] == "--":
                    moves.append(Move((row, column), (row, column-2), self.board))
            #Captures upward
            if row-1 >=1: #Bounds checking
                if (self.board[row-1][column-1][0] != '-') and (self.board[row-1][column-1][0] != 'l'): #Make sure not capturing self or empty
                    moves.append(Move((row, column), (row-1, column-1), self.board))
            #Captures downward 
            if row+1 <=14: #Bounds checking
                if (self.board[row+1][column-1][0] != '-') and (self.board[row+1][column-1][0] != 'l'): #Make sure not capturing self or empty
                    moves.append(Move((row, column), (row+1, column-1), self.board))                    

    def getRookMoves(self, row, column ,moves):
        directions = ((-1,0), (0,-1), (1,0), (0,1)) #up, left, down, right
        rookColor = self.board[row][column][0]
        for searchDirection in directions:
            for index in range(1, 14):
                endRow = row + searchDirection[0] * index
                endColumn = column + searchDirection[1] * index
                if self.isInsideGameGrid(endRow, endColumn):
                    endPiece = self.board[endRow][endColumn]
                    if endPiece == "--":
                        moves.append(Move((row, column), (endRow, endColumn), self.board))
                    elif endPiece[0] != rookColor:
                        moves.append(Move((row, column), (endRow, endColumn), self.board))
                        break
                    else:
                        break
                else:
                    break
       
    def getKnightMoves(self, row, column ,moves):
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1,-2), (1,2), (2,-1), (2,1))
        knightColor = self.board[row][column][0]
        for m in knightMoves:
            endRow = row + m[0]
            endColumn = column + m[1]
            if self.isInsideGameGrid(endRow, endColumn):
                endPiece = self.board[endRow][endColumn]
                if endPiece[0] != knightColor:
                    moves.append(Move((row, column), (endRow, endColumn), self.board))

    def getBishopMoves(self, row, column ,moves):
        directions = ((-1,-1), (-1,1), (1,-1), (1,1))
        BishopColor = self.board[row][column][0]
        for searchDirection in directions:
            for index in range(1, 14):
                endRow = row + searchDirection[0] * index
                endColumn = column + searchDirection[1] * index
                if self.isInsideGameGrid(endRow, endColumn):
                    endPiece = self.board[endRow][endColumn]
                    if endPiece == "--":
                        moves.append(Move((row, column), (endRow, endColumn), self.board))
                    elif endPiece[0] != BishopColor:
                        #print("Flag 30", row, column, endRow, endColumn)
                        moves.append(Move((row, column), (endRow, endColumn), self.board))
                        break
                    else:
                        break
                else:
                    break
    
    def getQueenMoves(self, row, column ,moves):
        self.getRookMoves(row, column, moves)
        self.getBishopMoves(row, column, moves)

    def getKingMoves(self, row, column, moves):
        kingMoves = ((-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1))
        kingColor = self.board[row][column][0]
        for i in range(8):
            endRow = row + kingMoves[i][0]
            endColumn = column + kingMoves[i][1]
            if self.isInsideGameGrid(endRow, endColumn):
                endPiece = self.board[endRow][endColumn]
                if endPiece[0] != kingColor:
                    moves.append(Move((row, column), (endRow, endColumn), self.board))


""" Move Class. Holds a move object as well as the chess notation."""                    
class Move:
    def __init__(self, startSq, endSq, board) -> None:
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endColumn = endSq[1]

        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endColumn]

        # Generates a number from the move to compare elsewhere through the overwritten = below to test for equality.
        self.moveID = self.getChessNotation()

    """ Overrides = """
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False
    
    ranksToRows = {"1":1, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "10":10, "11":11, "12":12, "13":13, "14":14}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}

    filesToCols = {"a":1, "b":2, "c":3, "d":4, "e":5, "f":6, "g":7, "h":8, "i":9, "j":10, "k":11, "l":12, "m":13, "n":14}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def getChessNotation(self):
        # We could eventually update this to real chess notation if we wanted
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endColumn)
        
    def getRankFile(self, r , c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
