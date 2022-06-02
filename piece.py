import pygame
import abc
import math


class Piece(abc.ABC):

    def __init__(self, xPos, yPos, team, graphicPath, pieceId, tilesList, surface):
        abc.ABC.__init__(self)
        self.x = xPos
        self.y = yPos
        self.team = team
        self.graphic = pygame.image.load(graphicPath) # picture of the piece
        self.graphic = pygame.transform.scale(self.graphic, (40, 40))
        self.rect = self.graphic.get_rect(center=(self.x, self.y))
        self.surface = surface
        self.captured = False
        self.selected = False
        self.moving = False
        self.pieceId = pieceId
        self.tilesList = tilesList
        self.tile = self.tilesList[math.trunc(self.y/50)][math.trunc(self.x/50)]
        self.validTiles = []  # contains a list of valid tiles to move to. Set by showLegalMoves

    def __str__(self):
        return f"{self.pieceId} at x: {self.x}, y: {self.y}"

    def draw(self):
        self.surface.blit(self.graphic, self.rect)
        self.x = self.rect.x
        self.y = self.rect.y

    @abc.abstractmethod
    def showLegalMoves(self):
        '''highlights all tiles that are legal moves and adds them to self.validTiles
        :param orient:
        '''
        pass

    @abc.abstractmethod
    def hideLegalMoves(self):
        pass

    def move(self, event):
        self.rect.move_ip(event.rel)

    def setPos(self, x, y, tile):
        '''Moves the piece. Returns True if tile moved successfully, False if not'''
        self.x = x
        self.y = y
        print(tile.rect.centery)
        self.rect.centerx = self.x
        self.rect.centery = self.y
        return True

    def getPosition(self):
        return self.x, self.y

    def getPieceId(self):
        return self.pieceId
