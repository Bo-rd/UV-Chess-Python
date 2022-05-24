import pygame
import abc


class Piece(abc.ABC):

    def __init__(self, xPos, yPos, team, graphicPath, pieceId, tilesList):
        abc.ABC.__init__(self)
        self.x = xPos
        self.y = yPos
        self.size = 50
        self.rect = None
        self.team = team
        self.graphic = pygame.image.load(graphicPath)  # picture of the piece
        self.captured = False
        self.selected = False
        self.pieceId = pieceId
        self.tilesList = tilesList
        self.validTiles = []  # contains a list of valid tiles to move to. Set by showLegalMoves

    def __str__(self):
        return f"{self.pieceId} at x: {self.x}, y: {self.y}"

    def draw(self, surface):
        pass

    @abc.abstractmethod
    def showLegalMoves(self):
        '''highlights all tiles that are legal moves and adds them to self.validTiles'''
        pass

    def setPos(self, x, y):
        '''Moves the piece. Returns True if tile moved successfully, False if not'''
        if x > 15 or y > 15:
            return False
        if x < 0 or y < 0:
            return False
        tile = self.tilesList[y][x]
        if tile not in self.validTiles:
            return False
        self.x = x
        self.y = y
        return True

    def getPosition(self):
        return self.x, self.y

    def getPieceId(self):
        return self.pieceId


class Test(Piece):

    def __init__(self, xPos, yPos, team, graphic, pieceId, tilesList):
        Piece.__init__(self, xPos, yPos, team, graphic, pieceId, tilesList)

    def showLegalMoves(self):
        pass