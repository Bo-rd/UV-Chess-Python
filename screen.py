import pygame
pygame.init()
background_colour = (169, 169, 169)
(width, height) = (800, 800)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('UV Chess')
screen.fill(background_colour)
pygame.display.flip()
running = True


class Tile:
    def __init__(self, xPos, yPos, color):
        self.x = xPos
        self.y = yPos
        self.color = color
        self.size = 50
        # Active is used to check for border or corner tiles
        self.active = True
        print("Made a tile at: " + str(self.x) + ", " + str(self.y))

    def draw(self, screen):
        gray = (169, 169, 169)
        black = (0, 0, 0)
        white = (255, 255, 255)
        blue = (0, 0, 255)
        surface = screen

        # Makes pattern on board
        if self.color == 1:
            pygame.draw.rect(surface, white, pygame.Rect(
                self.x*self.size, self.y*self.size, self.size, self.size))
        else:
            pygame.draw.rect(surface, black, pygame.Rect(
                self.x*self.size, self.y*self.size, self.size, self.size))

        # Makes gray corners and blue outline
        if self.x == 0 or self.y == 0 or self.x == 15 or self.y == 15:
            pygame.draw.rect(surface, blue, pygame.Rect(
                self.x*self.size, self.y*self.size, self.size, self.size))
            self.active = False
        if self.x > 0 and self.x < 4 and self.y > 0 and self.y < 4:
            pygame.draw.rect(surface, gray, pygame.Rect(
                self.x*self.size, self.y*self.size, self.size, self.size))
            self.active = False
        if self.x > 11 and self.x < 15 and self.y > 11 and self.y < 15:
            pygame.draw.rect(surface, gray, pygame.Rect(
                self.x*self.size, self.y*self.size, self.size, self.size))
            self.active = False

        if self.x > 0 and self.x < 4 and self.y > 11 and self.y < 15:
            pygame.draw.rect(surface, gray, pygame.Rect(
                self.x*self.size, self.y*self.size, self.size, self.size))
            self.active = False
        if self.x > 11 and self.x < 15 and self.y > 0 and self.y < 4:
            pygame.draw.rect(surface, gray, pygame.Rect(
                self.x*self.size, self.y*self.size, self.size, self.size))
            self.active = False
        # For some reason this draws to the screen, don't ask why I have no idea yet
        pygame.display.flip()

    def getPos(self):
        print(self.x + ", " + self.y)


board_made = False
while running:
    if board_made is False:
        rows = 16
        cols = 16
        tiles = [[0 for i in range(cols)] for j in range(rows)]
        for x in range(rows):
            for y in range(cols):
                tiles[y][x] = Tile(x, y, x % 2 + y % 2)
        for x in range(rows):
            for y in range(cols):
                tiles[y][x].draw(screen)
        board_made = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
