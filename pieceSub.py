from piece import Piece
import math


class King(Piece):
    '''
    The King may move one space in any direction,
    providing there isn't a friendly piece in the
    way. It may move slightly farther if castling
    with a Rook, which is covered in the Rook class.

    Cannot move into check, if in check, must move
    out of check.
    '''
    def __init__(self, xPos, yPos, team, graphicPath, pieceId, tilesList, surface):
        super().__init__(xPos, yPos, team, graphicPath, pieceId, tilesList, surface)
        self.hasMoved = False
        self.inCheck = False
        
    def showLegalMoves(self):
        pass

    def hideLegalMoves(self):
        pass


class Queen(Piece):
    '''
    A queen may move any direction, any length, so long
    as the path is clear. If an enemy is in the path, it 
    may be captured. Friendly pieces cannot be passed.
    '''
    def __init__(self, xPos, yPos, team, graphicPath, pieceId, tilesList, surface):
        super().__init__(xPos, yPos, team, graphicPath, pieceId, tilesList, surface)
        
    def showLegalMoves(self):
        pass

    def hideLegalMoves(self):
        pass


class Knight(Piece):
    '''
    L-shaped moves -> two left/right then one up/down, or
    two up/down then one left/right. Knights can jump
    friendly or enemy pieces, and only captures if it
    lands on an enemy piece.
    '''
    def __init__(self, xPos, yPos, team, graphicPath, pieceId, tilesList, surface):
        super().__init__(xPos, yPos, team, graphicPath, pieceId, tilesList, surface)
        
    def showLegalMoves(self):
        pass

    def hideLegalMoves(self):
        pass


class Bishop(Piece):
    '''
    The Bishop moves diagonally, any length, so long
    as the lane is clear to the destination. If there
    is an enemy on the path, it may be captured and the
    Bishop takes its place. 
    '''
    def __init__(self, xPos, yPos, team, graphicPath, pieceId, tilesList, surface):
        super().__init__(xPos, yPos, team, graphicPath, pieceId, tilesList, surface)
        
    def showLegalMoves(self):
        pass

    def hideLegalMoves(self):
        pass


class Rook(Piece):
    '''
    Straight lanes of any length - up/down/left/right.
    Captures on these lanes.

    If the King and Rook are unmoved, with empty
    space between them, the player may "Castle"
    in which case the King and Rook slide to meet
    eachother, then switch places, ending on the 
    opposite side they started on in relation to 
    eachother.

    Example on King side -> R _ _ K -> _ K R _
    Example on Queen side -> K _ _ _ R -> _ R K _ _ 
    '''
    def __init__(self, xPos, yPos, team, graphicPath, pieceId, tilesList, surface):
        super().__init__(xPos, yPos, team, graphicPath, pieceId, tilesList, surface)
        self.hasMoved = False
        
    def showLegalMoves(self):
        pass

    def hideLegalMoves(self):
        pass


class Pawn(Piece):
    '''
    May move two forward on first move, otherwise one forward.
    Captures diagonally. If pawn reaches the starting line of 
    an enemy team - it can be promoted to a Queen, Knight, Rook
    or Bishop.

    Pawns can also capture "En Passant". If an enemy Pawn moves 
    foward two spaces on its first move, and another pawn then
    moves diagonally to the space that was skipped, the enemy
    Pawn is captured.
    '''
    def __init__(self, xPos, yPos, team, graphicPath, pieceId, tilesList, surface):
        super().__init__(xPos, yPos, team, graphicPath, pieceId, tilesList, surface)
        self.hasMoved = False
        self.start = True

    def showLegalMoves(self):
        if self.start:
            moveAmt = 100
        else:
            moveAmt = 50
        if self.team == "White":
            print("showing legal moves")
            print(f"{self.x}, {self.y}")
            self.tile.changeColor(surface=self.surface, color=(0, 255, 0))
            x, y = self.x, self.y

            x -= moveAmt
        elif self.team == "Black":
            print("showing legal moves")
            print(f"{self.x}, {self.y}")
            self.tile.changeColor(surface=self.surface, color=(0, 255, 0))
            x, y = self.x, self.y

            x += moveAmt
        elif self.team == "Red":
            print("showing legal moves")
            print(f"{self.x}, {self.y}")
            self.tile.changeColor(surface=self.surface, color=(0, 255, 0))
            x, y = self.x, self.y

            y -= moveAmt
        elif self.team == "Blue":
            print("showing legal moves")
            print(f"{self.x}, {self.y}")
            self.tile.changeColor(surface=self.surface, color=(0, 255, 0))
            x, y = self.x, self.y

            y += moveAmt
        else:
            return False

        if self.start:
            print("start")
            if self.team == "White":
                tile1 = self.tilesList[math.trunc(y / 50)][math.trunc(x / 50)]
                tile2 = self.tilesList[math.trunc(y / 50)][math.trunc((x + 50) / 50)]
            elif self.team == "Black":
                tile1 = self.tilesList[math.trunc(y / 50)][math.trunc(x / 50)]
                tile2 = self.tilesList[math.trunc(y / 50)][math.trunc((x - 50) / 50)]
            elif self.team == "Red":
                tile1 = self.tilesList[math.trunc(y / 50)][math.trunc(x / 50)]
                tile2 = self.tilesList[math.trunc((y + 50) / 50)][math.trunc(x / 50)]
            elif self.team == "Blue":
                tile1 = self.tilesList[math.trunc(y / 50)][math.trunc(x / 50)]
                tile2 = self.tilesList[math.trunc((y - 50) / 50)][math.trunc(x / 50)]
            else:
                return False
            tile1.changeColor(self.surface, (0, 255, 0))
            tile2.changeColor(self.surface, (0, 255, 0))
            self.validTiles.append(tile1)
            self.validTiles.append(tile2)
            self.start = False

        else:
            newTile = self.tilesList[math.trunc(y / 50)][math.trunc(x / 50)]
            if newTile is self.tile:
                print("Same")
            newTile.changeColor(self.surface, (0, 255, 0))
            print(newTile.color)
            self.validTiles.append(newTile)

    def hideLegalMoves(self):
        self.tile.changeColor(surface=self.surface, color=self.tile.color)
        for tile in self.validTiles:
            print(tile.x, tile.y)
            tile.changeColor(surface=self.surface, color=tile.color)
            self.validTiles = []

