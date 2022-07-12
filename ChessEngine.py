"""
4 player Chess - Python
Summer 2022
-
Andrew Pritchett -- Christopher Wilkinson -- Joshua Kitchen -- Max Diamond -- Seth Bird
-
#GameState
#Move Log
#Calculate Valid Moves
"""


import copy

class ChessPlayerObject:
    """ The Node type object that holds player's info for our doubly linked list """
    def __init__(self, name, gameColor, colorCode, number, nextPlayer = None, previousPlayer = None) -> None:
       self.name = name
       self.gameColor = gameColor
       self.colorCode = colorCode
       self.number = number
       self.nextPlayer = nextPlayer
       self.previousPlayer = previousPlayer

       self.canCastle = True

class GamePlayers:
    """ Our doubly linked list """
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
        self.currentPlayer.previousPlayer.nextPlayer = self.currentPlayer

""" Implementing/initiating the player list """
userPlayerNames = ["Alpha", "Bravo", "Charlie", "Delta"] # If we want to implement user submitted usernames in the future we could add them to a list like this

# This creates a linked list to keep the player's info and to make switching easier.
playerList = GamePlayers()
whitePlayer = ChessPlayerObject(userPlayerNames[0], "White", "w", 0, nextPlayer = None,  previousPlayer = None)
redPlayer = ChessPlayerObject(userPlayerNames[1], "Red", "r", 1, nextPlayer = None,  previousPlayer = whitePlayer)
blackPlayer = ChessPlayerObject(userPlayerNames[2], "Black", "b", 2, nextPlayer = None,  previousPlayer = redPlayer)
bluePlayer = ChessPlayerObject(userPlayerNames[3], "Blue", "l", 3, nextPlayer = None,  previousPlayer = blackPlayer)

# Since some objects are not created until after these needed to be manually put in.
whitePlayer.nextPlayer = redPlayer
redPlayer.nextPlayer = blackPlayer
blackPlayer.nextPlayer = bluePlayer
bluePlayer.nextPlayer = whitePlayer
whitePlayer.previousPlayer = bluePlayer

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
            ["--","rR","rp","--","--","--","--","--","--","--","--","--","--","lp","lR","--"],
            ["--","rN","rp","--","--","--","--","--","--","--","--","--","--","lp","lN","--"],
            ["--","rB","rp","--","--","--","--","--","--","--","--","--","--","lp","lB","--"],
            ["--","rQ","rp","--","--","--","--","--","--","--","--","--","--","lp","lQ","--"],
            ["--","rK","rp","--","--","--","--","--","--","--","--","--","--","lp","lK","--"],
            ["--","rB","rp","--","--","--","--","--","--","--","--","--","--","lp","lB","--"],
            ["--","rN","rp","--","--","--","--","--","--","--","--","--","--","lp","lN","--"],
            ["--","rR","rp","--","--","--","--","--","--","--","--","--","--","lp","lR","--"],
            ["--","--","--","--","--","--","--","--","--","--","--","--","--","--","--","--"],
            ["--","--","--","--","wp","wp","wp","wp","wp","wp","wp","wp","--","--","--","--"],
            ["--","--","--","--","wR","wN","wB","wQ","wK","wB","wN","wR","--","--","--","--"],
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

    def canCastleLeft(self, color):
        """
        Determine if the given color of team can castle
        to the left. Called by getKingMoves().
        """
        if color == 'w':
            # verify the king and rook are in the proper locations
            if self.board[14][4] == "wR" and self.board[14][8] == "wK":
                for i in range(5,8):
                    # verify that the space between the rook and king
                    # is empty
                    if self.board[14][i] != "--":
                        return False
                return True
        
        elif color == 'r':
            if self.board[4][1] == "rR" and self.board[8][1] == "rK":
                for i in range(5,8):
                    if self.board[i][1] != "--":
                        return False
                return True

        elif color == 'b':
            if self.board[1][11] == "bR" and self.board[1][8] == "bK":
                for i in range(9,11):
                    if self.board[1][i] != "--":
                        return False
                return True

        else: # blue
            if self.board[11][14] == "lR" and self.board[8][14] == "lK":
                for i in range(9,11):
                    if self.board[i][14] != "--":
                        return False
                return True

    def canCastleRight(self, color):
        """
        Determine if the given color of team can castle
        to the right. Called by getKingMoves().
        """
        if color == 'w':
            if self.board[14][11] == "wR" and self.board[14][8] == "wK":
                for i in range(9,11):
                    if self.board[14][i] != "--":
                        return False
                return True
        
        elif color == 'r':
            if self.board[11][1] == "rR" and self.board[8][1] == "rK":
                for i in range(9,11):
                    if self.board[i][1] != "--":
                        return False
                return True

        elif color == 'b':
            if self.board[1][4] == "bR" and self.board[1][8] == "bK":
                for i in range(5,8):
                    if self.board[1][i] != "--":
                        return False
                return True

        else: # blue
            if self.board[4][14] == "lR" and self.board[8][14] == "lK":
                for i in range(5,8):
                    if self.board[i][14] != "--":
                        return False
                return True

    def updateKing(self, move):
        """
        Updates the King's Position tuple if needed. Also
        check if a castling move was made - if so, move the 
        appropriate rook and add the move to the move list.
        """
        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.endRow, move.endCol)

            whitePlayer.canCastle = False

            direction = move.endCol - move.startCol
            if direction == -2:
                rookMove = Move((14,4), (14,7), self.board)
                self.board[rookMove.startRow][rookMove.startCol] = "--"
                self.board[rookMove.endRow][rookMove.endCol] = rookMove.pieceMoved
                self.moveLog.append(rookMove) #logs the move

            elif direction == 2:
                rookMove = Move((14,11), (14,9), self.board)
                self.board[rookMove.startRow][rookMove.startCol] = "--"
                self.board[rookMove.endRow][rookMove.endCol] = rookMove.pieceMoved
                self.moveLog.append(rookMove) #logs the move
                
        if move.pieceMoved == "rK":
            self.redKingLocation = (move.endRow, move.endCol)

            redPlayer.canCastle = False

            direction = move.endRow - move.startRow
            if direction == -2:
                rookMove = Move((4,1), (7,1), self.board)
                self.board[rookMove.startRow][rookMove.startCol] = "--"
                self.board[rookMove.endRow][rookMove.endCol] = rookMove.pieceMoved
                self.moveLog.append(rookMove) #logs the move

            elif direction == 2:
                rookMove = Move((11,1), (9,1), self.board)
                self.board[rookMove.startRow][rookMove.startCol] = "--"
                self.board[rookMove.endRow][rookMove.endCol] = rookMove.pieceMoved
                self.moveLog.append(rookMove) #logs the move

        if move.pieceMoved == "bK":
            self.blackKingLocation = (move.endRow, move.endCol)

            blackPlayer.canCastle = False

            direction = move.endCol - move.startCol
            if direction == -2:
                rookMove = Move((1,4), (1,7), self.board)
                self.board[rookMove.startRow][rookMove.startCol] = "--"
                self.board[rookMove.endRow][rookMove.endCol] = rookMove.pieceMoved
                self.moveLog.append(rookMove) #logs the move

            elif direction == 2:
                rookMove = Move((1,11), (1,9), self.board)
                self.board[rookMove.startRow][rookMove.startCol] = "--"
                self.board[rookMove.endRow][rookMove.endCol] = rookMove.pieceMoved
                self.moveLog.append(rookMove) #logs the move

        if move.pieceMoved == "lK":
            self.blueKingLocation = (move.endRow, move.endCol)
            
            bluePlayer.canCastle = False

            direction = move.endRow - move.startRow
            if direction == -2: # right castle
                rookMove = Move((4,14), (7,14), self.board)
                self.board[rookMove.startRow][rookMove.startCol] = "--"
                self.board[rookMove.endRow][rookMove.endCol] = rookMove.pieceMoved
                self.moveLog.append(rookMove) #logs the move

            elif direction == 2: # left castle
                rookMove = Move((11,14), (9,14), self.board)
                self.board[rookMove.startRow][rookMove.startCol] = "--"
                self.board[rookMove.endRow][rookMove.endCol] = rookMove.pieceMoved
                self.moveLog.append(rookMove) #logs the move

    
    def makeMove(self, move):
        """ Moves a chess piece """
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) #logs the move
        
        self.updateKing(move) # Checks and Updates the King's Position tuple if needed.

        playerList.nextPlayer()

        print(self.currentPlayerPrintout[playerList.currentPlayer.number]) # Prints new players turn
    
    
    def undoMove(self):
        """ Undo the last move """
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured

            self.updateKing(move) # Checks and Updates the King's Position tuple if needed.

            playerList.previousPlayer()
            
            print(self.currentPlayerPrintout[playerList.currentPlayer.number]) # Prints new players turn


    def getValidMovesHelper(self, move):
        """Helper function for getValidMoves. Does same thing as makeMove() but does not change player and log and stuff."""
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.updateKing(move)


    def getValidMoves(self):
        """All moves considering checks"""
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

            currPlayer = playerList.currentPlayer

            playerList.nextPlayer() # move to the next player
            while playerList.currentPlayer != currPlayer:
                attackerMoveList += self.getAllPossibleMoves()
                playerList.nextPlayer() # increment

            # loop ends at the current player

            testFlag = True
            # Loops through potential other player's moves
            for attackerMove in attackerMoveList:
                # If an other piece puts you into check....
                if self.inCheck(attackerMove.endRow, attackerMove.endCol): 
                    testFlag = False
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

        
        if len(validMoves) > 0:
            #FIXME there are some random moves making it through
            for move in validMoves:
                print(move.getChessNotation())
            return validMoves

        # for checkmate
        else:
            playerSymbol = playerList.currentPlayer.colorCode
            playerNum = playerList.currentPlayer.number

            playerList.removePlayer()

            # remove from turn printout roster
            self.currentPlayerPrintout.pop(playerNum)

            # remove king location
            if playerSymbol == 'w':
                self.whiteKingLocation = (0,0)
            elif playerSymbol == 'r':
                self.redKingLocation = (0,0)
            elif playerSymbol == 'b':
                self.blackKingLocation = (0,0)
            else:
                self.blueKingLocation = (0,0)

            # remove players pieces from board
            for row in range(len(self.board)):
                for col in range(len(self.board[0])):
                    if self.board[row][col][0] == playerSymbol:
                        self.board[row][col] = "--"
            
            print(self.currentPlayerPrintout[playerList.currentPlayer.number]) # Prints new players turn

            return self.getValidMoves() # get moves for next player

    def inCheck(self, row, column):
        """ Determines if the current player is in check """
        if playerList.currentPlayer.number == 0:
            return (row == self.whiteKingLocation[0]) and (column == self.whiteKingLocation[1])
        
        if playerList.currentPlayer.number == 1:
            return (row == self.redKingLocation[0]) and (column == self.redKingLocation[1])   

        if playerList.currentPlayer.number == 2:
            return (row == self.blackKingLocation[0]) and (column == self.blackKingLocation[1])

        if playerList.currentPlayer.number == 3:
            return (row == self.blueKingLocation[0]) and (column == self.blueKingLocation[1])

    
    def getAllPossibleMoves(self):
        """All moves without consideriding checks"""
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
    def isInsideGameGrid(self, endRow, endCol):
        if 1 <= endRow <= 14 and 1 <= endCol <= 14 and not ((endRow <= 3 and endCol <= 3) or (endRow >= 12 and endCol <= 3) or (endRow <= 3 and endCol >= 12) or (endRow >= 12 and endCol >= 12)):
            return True
        return False

    def getPawnMoves(self, row, column, moves):
        """
        Get all the pawn moves for the pawn located at row, col and add these moves to the list
        """

        ''' Player 0 is white. This logic is for WHITE Pawns. '''
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

        ''' Player 1 is red. This logic is for RED Pawns. '''
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

        ''' Player 2 is black. This logic is for BLACK Pawns. '''
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

        ''' Player 3 is blue. This logic is for BLUE Pawns. '''
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
                endCol = column + searchDirection[1] * index
                if self.isInsideGameGrid(endRow, endCol):
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((row, column), (endRow, endCol), self.board))
                    elif endPiece[0] != rookColor:
                        moves.append(Move((row, column), (endRow, endCol), self.board))
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
            endCol = column + m[1]
            if self.isInsideGameGrid(endRow, endCol):
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != knightColor:
                    moves.append(Move((row, column), (endRow, endCol), self.board))

    def getBishopMoves(self, row, column ,moves):
        directions = ((-1,-1), (-1,1), (1,-1), (1,1))
        BishopColor = self.board[row][column][0]
        for searchDirection in directions:
            for index in range(1, 14):
                endRow = row + searchDirection[0] * index
                endCol = column + searchDirection[1] * index
                if self.isInsideGameGrid(endRow, endCol):
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((row, column), (endRow, endCol), self.board))
                    elif endPiece[0] != BishopColor:
                        #print("Flag 30", row, column, endRow, endCol)
                        moves.append(Move((row, column), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break
    
    def getQueenMoves(self, row, column ,moves):
        self.getRookMoves(row, column, moves)
        self.getBishopMoves(row, column, moves)

    def getKingMoves(self, row, column ,moves):
        kingMoves = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
        kingColor = self.board[row][column][0]

        # adds castling moves for each color
        if kingColor == 'w':
            if self.canCastleLeft('w'):
                kingMoves.append((0,-2))
            if self.canCastleRight('w'):
                kingMoves.append((0,2))

        elif kingColor == 'r':
            if self.canCastleLeft('r'):
                kingMoves.append((-2,0))
            if self.canCastleRight('r'):
                kingMoves.append((2,0))

        elif kingColor == 'b':
            # upside down version of white
            if self.canCastleLeft('b'):
                kingMoves.append((0,2))
            if self.canCastleRight('b'):
                kingMoves.append((0,-2))

        else: # blue
            if self.canCastleLeft('l'):
                kingMoves.append((2,0))
            if self.canCastleRight('l'):
                kingMoves.append((-2,0))

        for i in range(len(kingMoves)):
            endRow = row + kingMoves[i][0]
            endCol = column + kingMoves[i][1]
            if self.isInsideGameGrid(endRow, endCol):
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != kingColor:
                    moves.append(Move((row, column), (endRow, endCol), self.board))

""" Move Class. Holds a move object as well as the chess notation."""                    
class Move():
    def __init__(self, startSq, endSq, board) -> None:
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]

        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]

        # Generates a number from the move to compare elsewhere through the overwritten = below to test for equality.
        self.moveID = self.getChessNotation()

    """ Overrides = """
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False
    
    ranksToRows = {"0":0, "1":1, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "10":10, "11":11, "12":12, "13":13, "14":14, "15":15}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}

    filesToCols = {"a":1, "b":2, "c":3, "d":4, "e":5, "f":6, "g":7, "h":8, "i":9, "j":10, "k":11, "l":12, "m":13, "n":14, "o":15}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def getChessNotation(self):
        # We could eventually update this to real chess notation if we wanted
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
        
    def getRankFile(self, r , c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
