import pygame
import abc


class Piece(abc.ABC):

    def __init__(self, xPos, yPos, team, graphicPath, pieceId, tilesList, surface):
        abc.ABC.__init__(self)
        self.x = xPos
        self.y = yPos
        self.team = team
        self.graphic = pygame.image.load(graphicPath) # picture of the piece
        self.graphic = pygame.transform.scale(self.graphic, (35, 35))
        self.rect = self.graphic.get_rect(center=(self.x, self.y))
        self.surface = surface
        self.captured = False
        self.selected = False
        self.moving = False
        self.pieceId = pieceId
        self.tilesList = tilesList
        self.validTiles = []  # contains a list of valid tiles to move to. Set by showLegalMoves

    def __str__(self):
        return f"{self.pieceId} at x: {self.x}, y: {self.y}"

    def draw(self):
        self.surface.blit(self.graphic, self.rect)
        self.x = self.rect.x
        self.y = self.rect.y

    @abc.abstractmethod
    def showLegalMoves(self):
        '''highlights all tiles that are legal moves and adds them to self.validTiles'''
        pass

    def move(self, event):
        self.rect.move_ip(event.rel)

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
        self.surface.blit(self.graphic, (self.x, self.y))
        return True

    def getPosition(self):
        return self.x, self.y

    def getPieceId(self):
        return self.pieceId


class Test(Piece):

    def __init__(self, xPos, yPos, team, graphicPath, pieceId, tilesList, surface):
        Piece.__init__(self, xPos, yPos, team, graphicPath, pieceId, tilesList, surface)

    def showLegalMoves(self):
        pass
