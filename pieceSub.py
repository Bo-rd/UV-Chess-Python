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
    def __init__(self, xPos, yPos, team, graphicPath, pieceId, surface):
        super().__init__(xPos, yPos, team, graphicPath, pieceId, surface)
        self.hasMoved = False
        self.inCheck = False

    def getLegalMoves(self):
        pass

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
    def __init__(self, xPos, yPos, team, graphicPath, pieceId, surface):
        super().__init__(xPos, yPos, team, graphicPath, pieceId, surface)

    def getLegalMoves(self):
        pass

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
    def __init__(self, xPos, yPos, team, graphicPath, pieceId, surface):
        super().__init__(xPos, yPos, team, graphicPath, pieceId, surface)

    def getLegalMoves(self):
        pass

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
    def __init__(self, xPos, yPos, team, graphicPath, pieceId, surface):
        super().__init__(xPos, yPos, team, graphicPath, pieceId, surface)

    def getLegalMoves(self):
        pass

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
    def __init__(self, xPos, yPos, team, graphicPath, pieceId, surface):
        super().__init__(xPos, yPos, team, graphicPath, pieceId, surface)

    def getLegalMoves(self):
        pass

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
    def __init__(self, xPos, yPos, team, graphicPath, pieceId, surface):
        super().__init__(xPos, yPos, team, graphicPath, pieceId, surface)
        self.start = True

    def getLegalMoves(self):
        pass

    def showLegalMoves(self):
        pass

    def hideLegalMoves(self):
        self.tile.changeColor(surface=self.surface, color=self.tile.color)
        for tile in self.validTiles:
            tile.changeColor(surface=self.surface, color=tile.color)
            self.validTiles = []
