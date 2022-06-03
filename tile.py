import pygame


class Tile:
    def __init__(self, xPos, yPos, color):
        self.x = xPos
        self.y = yPos
        self.color = color
        self.size = 50
        self.rect = None
        # Active is used to check for border or corner tiles
        self.active = True
        self.hasPiece = False
        self.piece = None
        self.rect = pygame.Rect(xPos, yPos, self.size, self.size)
        self.clicked = False
        self.highlighted = False
        # print("Made a tile at: " + str(self.x) + ", " + str(self.y))

    def changeColor(self, surface, color):
        if color == 1:
            self.rect = pygame.draw.rect(surface, (255, 255, 255), pygame.Rect(
                self.x * self.size, self.y * self.size, self.size, self.size))
        elif color == 2:
            self.rect = pygame.draw.rect(surface, (0, 0, 0), pygame.Rect(
                self.x * self.size, self.y * self.size, self.size, self.size))
        else:
            self.rect = pygame.draw.rect(surface, color, pygame.Rect(
                self.x * self.size, self.y * self.size, self.size, self.size))

    def putPiece(self, pieceToPlace):
        self.piece = pieceToPlace
        self.hasPiece = True

    def removePiece(self):
        self.piece = None
        self.hasPiece = False

    def getHasPiece(self):
        return self.hasPiece

    def getPos(self):
        return (str(self.x) + ", " + str(self.y))

    def getPiece(self):
        if self.hasPiece:
            return self.piece

    def tick(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.highlighted = True
        else:
            self.highlighted = False

    def render(self, screen):
        gray = (169, 169, 169)
        black = (0, 0, 0)
        white = (255, 255, 255)
        blue = (0, 0, 255)
        yellow = (255, 255, 0)
        surface = screen

        # Makes pattern on board
        if self.color == 1:
            self.rect = pygame.draw.rect(surface, white, pygame.Rect(
                self.x*self.size, self.y*self.size, self.size, self.size))
        else:
            self.rect = pygame.draw.rect(surface, black, pygame.Rect(
                self.x*self.size, self.y*self.size, self.size, self.size))
            # Makes gray corners and blue outline
        if self.x == 0 or self.y == 0 or self.x == 15 or self.y == 15:
            self.rect = pygame.draw.rect(surface, blue, pygame.Rect(
                self.x*self.size, self.y*self.size, self.size, self.size))
            self.active = False
        elif self.x > 0 and self.x < 4 and self.y > 0 and self.y < 4:
            self.rect = pygame.draw.rect(surface, gray, pygame.Rect(
                self.x*self.size, self.y*self.size, self.size, self.size))
            self.active = False
        elif self.x > 11 and self.x < 15 and self.y > 11 and self.y < 15:
            self.rect = pygame.draw.rect(surface, gray, pygame.Rect(
                self.x*self.size, self.y*self.size, self.size, self.size))
            self.active = False

        elif self.x > 0 and self.x < 4 and self.y > 11 and self.y < 15:
            self.rect = pygame.draw.rect(surface, gray, pygame.Rect(
                self.x*self.size, self.y*self.size, self.size, self.size))
            self.active = False
        elif self.x > 11 and self.x < 15 and self.y > 0 and self.y < 4:
            self.rect = pygame.draw.rect(surface, gray, pygame.Rect(
                self.x*self.size, self.y*self.size, self.size, self.size))
            self.active = False
        elif self.highlighted:
            pygame.draw.rect(surface, yellow, pygame.Rect(
                self.x*self.size, self.y*self.size, self.size, self.size))
        # For some reason this draws to the screen, don't ask why I have no idea yet
