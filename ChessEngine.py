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

class ChesPlayerObject:
    def __init__(self, name, gameColor, colorCode, number, nextPlayer = None, previousPlayer = None) -> None:
       self.name = name #"A Player"
       self.gameColor = gameColor #"Blue"
       self.colorCode = colorCode
       self.number = number
       self.nextPlayer = nextPlayer
       self.previousPlayer = previousPlayer

       self.canCastleLeft = True
       self.canCastleRight = True

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
whitePlayer = ChesPlayerObject(userPlayerNames[0], "White", "w", 0, nextPlayer = None,  previousPlayer = None)
bluePlayer = ChesPlayerObject(userPlayerNames[1], "Blue", "l", 1, nextPlayer = None,  previousPlayer = whitePlayer)
blackPlayer = ChesPlayerObject(userPlayerNames[2], "Black", "b", 2, nextPlayer = None,  previousPlayer = bluePlayer)
redPlayer = ChesPlayerObject(userPlayerNames[3], "Red", "r", 3, nextPlayer = None,  previousPlayer = blackPlayer)

# Since some objects are not created until after these needed to be manually put in.
whitePlayer.nextPlayer = bluePlayer
bluePlayer.nextPlayer = blackPlayer
blackPlayer.nextPlayer = redPlayer
redPlayer.nextPlayer = whitePlayer
whitePlayer.previousPlayer = redPlayer

# This starts off the doubly linked list with the starting player.
playerList.currentPlayer = whitePlayer

class GameState():
    def __init__(self) -> None:
        # w = White, l = Blue, b = Black, r = Red
        # R = Rook, N = Knight, B = Bishop, Q = Queen, K = King, p = Pawn
        # -- denotes an empty square
        self.board = [
            ["--","--","--","--","--","--","--","--","--","--","--","--","--","--","--","--"],
            ["--","--","--","--","bR","bN","bB","bQ","bK","bB","bN","bR","--","--","--","--"],
            ["--","--","--","--","bp","bp","bp","bp","bp","bp","bp","bp","--","--","--","--"],
            ["--","--","--","--","--","--","--","--","--","--","--","--","--","--","--","--"],
            ["--","lR","lp","--","--","--","--","--","--","--","--","--","--","rp","rR","--"],
            ["--","lN","lp","--","--","--","--","--","--","--","--","--","--","rp","rN","--"],
            ["--","lB","lp","--","--","--","--","--","--","--","--","--","--","rp","rB","--"],
            ["--","lQ","lp","--","--","--","--","--","--","--","--","--","--","rp","rQ","--"],
            ["--","lK","lp","--","--","--","--","--","--","--","--","--","--","rp","rK","--"],
            ["--","lB","lp","--","--","--","--","--","--","--","--","--","--","rp","rB","--"],
            ["--","lN","lp","--","--","--","--","--","--","--","--","--","--","rp","rN","--"],
            ["--","lR","lp","--","--","--","--","--","--","--","--","--","--","rp","rR","--"],
            ["--","--","--","--","--","--","--","--","--","--","--","--","--","--","--","--"],
            ["--","--","--","--","wp","wp","wp","wp","wp","wp","wp","wp","--","--","--","--"],
            ["--","--","--","--","wR","wN","wB","wQ","wK","wB","wN","wR","--","--","--","--"],
            ["--","--","--","--","--","--","--","--","--","--","--","--","--","--","--","--"]
        ]

        self.whiteKingLocation = (14, 8)
        self.blueKingLocation = (8, 1)
        self.blackKingLocation = (1, 8)
        self.redKingLocation = (8, 14)

        self.moveFunctions = {'p': self.getPawnMoves, "R": self.getRookMoves, "N": self.getKnightMoves, "B": self.getBishopMoves, "Q": self.getQueenMoves, "K": self.getKingMoves}
        self.currentPlayerPrintout = {0:"It is White's Turn", 1:"It is Blue's Turn", 2:"It is Black's Turn", 3:"It is Red's Turn"}
        print(self.currentPlayerPrintout[playerList.currentPlayer.number]) # Prints out initial starting player
        self.moveLog = []
        # Print player name change on change

    def updateKing(self, move):
        # Updates the King's Position tuple if needed.
        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.endRow, move.endColumn)
        if move.pieceMoved == "lK":
            self.blueKingLocation = (move.endRow, move.endColumn)
        if move.pieceMoved == "bK":
            self.blackKingLocation = (move.endRow, move.endColumn)
        if move.pieceMoved == "rK":
            self.redKingLocation = (move.endRow, move.endColumn)

    """ Moves a chess piece """
    def makeMove(self, move):
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

    """All moves considering checks"""
    def getValidMoves(self):
        """
        boardBackup = copy.deepcopy(self.board) #Copy of the current game board.
        """
        moves = self.getAllPossibleMoves() # Generates the move list for the player like normal.
        """
        attackerMoveList = [] # To hold potential attacker moves.
        for i in range(len(moves)-1, -1, -1): # Goes through that list backwards.
            self.getValidMovesHelper(moves[i]) # Moves one piece per loop of the origin color.

            # Adds the next three player's moves into the attackerMoveList list.
            playerList.nextPlayer() 
            attackerMoveList += self.getAllPossibleMoves()
            playerList.nextPlayer() 
            attackerMoveList += self.getAllPossibleMoves()
            playerList.nextPlayer() 
            attackerMoveList += self.getAllPossibleMoves()
            playerList.nextPlayer() #The fourth one just returns back to the right player order.

            # Loops through potential other player's moves
            for attackerMove in attackerMoveList:                
                if self.inCheck(attackerMove.endRow, attackerMove.endColumn): # If an other piece puts you into check....
                    moves.remove(moves[-1]) #remove the potential move from the move list
                    break # Short circut evaluation. No need to keep calculating.

            self.board = copy.deepcopy(boardBackup) # Restores the board.
        self.board = copy.deepcopy(boardBackup) # Restores the board.
        """
        return moves 

    """ Determines if the current player is in check """
    def inCheck(self, row, column):
        if playerList.currentPlayer.number == 0:
            return (row == self.whiteKingLocation[0]) and (column == self.whiteKingLocation[1])
        
        if playerList.currentPlayer.number == 1:
            return (row == self.blueKingLocation[0]) and (column == self.blueKingLocation[1])   

        if playerList.currentPlayer.number == 2:
            return (row == self.blackKingLocation[0]) and (column == self.blackKingLocation[1])

        if playerList.currentPlayer.number == 3:
            return (row == self.redKingLocation[0]) and (column == self.redKingLocation[1])


    """All moves without consideriding checks"""
    def getAllPossibleMoves(self):
        moves = []
        for row in range(len(self.board)): 
            for column in range(len(self.board[row])):
                # This calculates moves only for the current players pieces.
                turn = self.board[row][column][0] # Index 0 is the color/player position on the board.
                if (turn == 'w' and playerList.currentPlayer.number == 0) or (turn == 'l' and playerList.currentPlayer.number == 1) or (turn == 'b' and playerList.currentPlayer.number == 2) or (turn == 'r' and playerList.currentPlayer.number == 3):
                    piece = self.board[row][column][1] # Index 1 is the piece type.
                    self.moveFunctions[piece](row, column, moves) # Calls move function for specific piece
        return moves

    # Returnes True if coords are in the 14X14 board AND not in one of those corner spots.
    def onGameBoardSquare(self, endRow, endColumn):
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

        """ Player 1 is blue. This logic is for BLUE Pawns. """
        if playerList.currentPlayer.number == 1: 
            if self.board[row][column+1] == "--":
                moves.append(Move((row, column), (row, column+1), self.board))
                if column == 2 and self.board[row][column+2] == "--":
                    moves.append(Move((row, column), (row, column+2), self.board))
            #Captures upward
            if row-1 >=1: #Bounds checking
                if (self.board[row-1][column+1][0] != '-') and (self.board[row-1][column+1][0] != 'l'): #Make sure not capturing self or empty
                    moves.append(Move((row, column), (row-1, column+1), self.board))
            #Captures downward 
            if row+1 <=14: #Bounds checking
                if (self.board[row+1][column+1][0] != '-') and (self.board[row+1][column+1][0] != 'l'): #Make sure not capturing self or empty
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

        """ Player 3 is red. This logic is for RED Pawns. """
        if playerList.currentPlayer.number == 3: 
            if self.board[row][column-1] == "--":
                moves.append(Move((row, column), (row, column-1), self.board))
                if column == 13 and self.board[row][column-2] == "--":
                    moves.append(Move((row, column), (row, column-2), self.board))
            #Captures upward
            if row-1 >=1: #Bounds checking
                if (self.board[row-1][column-1][0] != '-') and (self.board[row-1][column-1][0] != 'r'): #Make sure not capturing self or empty
                    moves.append(Move((row, column), (row-1, column-1), self.board))
            #Captures downward 
            if row+1 <=14: #Bounds checking
                if (self.board[row+1][column-1][0] != '-') and (self.board[row+1][column-1][0] != 'r'): #Make sure not capturing self or empty
                    moves.append(Move((row, column), (row+1, column-1), self.board))                    

    def getRookMoves(self, row, column ,moves):
        directions = ((-1,0), (0,-1), (1,0), (0,1)) #up, left, down, right
        rookColor = self.board[row][column][0]
        for searchDirection in directions:
            for index in range(2, 15):
                endRow = row + searchDirection[0] * index
                endColumn = column + searchDirection[1] * index
                if self.onGameBoardSquare(endRow, endColumn):
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
            if self.onGameBoardSquare(endRow, endColumn):
                endPiece = self.board[endRow][endColumn]
                if endPiece[0] != knightColor:
                    moves.append(Move((row, column), (endRow, endColumn), self.board))

    def getBishopMoves(self, row, column ,moves):
        directions = ((-1,-1), (-1,1), (1,-1), (1,1))
        BishopColor = self.board[row][column][0]
        for searchDirection in directions:
            for index in range(2, 15):
                endRow = row + searchDirection[0] * index
                endColumn = column + searchDirection[1] * index
                if self.onGameBoardSquare(endRow, endColumn):
                    endPiece = self.board[endRow][endColumn]
                    if endPiece == "--":
                        moves.append(Move((row, column), (endRow, endColumn), self.board))
                    elif endPiece[0] != BishopColor:
                        moves.append(Move((row, column), (endRow, endColumn), self.board))
                        break
                    else:
                        break
                else:
                    break
    
    def getQueenMoves(self, row, column ,moves):
        self.getRookMoves(row, column, moves)
        self.getBishopMoves(row, column, moves)

    def getKingMoves(self, row, column ,moves):
        kingMoves = ((-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1))
        kingColor = self.board[row][column][0]
        for i in range(8):
            endRow = row + kingMoves[i][0]
            endColumn = column + kingMoves[i][1]
            if self.onGameBoardSquare(endRow, endColumn):
                endPiece = self.board[endRow][endColumn]
                if endPiece[0] != kingColor:
                    moves.append(Move((row, column), (endRow, endColumn), self.board))

""" Move Class. Holds a move object as well as the chess notation."""                    
class Move():
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
    
    ranksToRows = {"1":14, "2":13, "3":12, "4":11, "5":10, "6":9, "7":8, "8":7, "9":6, "10":5, "11":4, "12":3, "13":2, "14":1}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}

    filesToCols = {"a":1, "b":2, "c":3, "d":4, "e":5, "f":6, "g":7, "h":8, "i":9, "j":10, "k":11, "l":12, "m":13, "n":14}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def getChessNotation(self):
        # We could eventually update this to real chess notation if we wanted
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endColumn)
        
    def getRankFile(self, r , c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
