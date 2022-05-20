import pygame
pygame.init()
background_colour = (169, 169, 169)
(width, height) = (800, 600)
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
        print("Made a tile at: " + str(self.x) + ", " + str(self.y))

    def draw(self, screen):
        surface = screen
        if self.color == 1:
            pygame.draw.rect(surface, (255, 255, 255), pygame.Rect(
                self.x*30, self.y*30, 30, 30))
        else:
            pygame.draw.rect(surface, (0, 0, 0), pygame.Rect(
                self.x*30, self.y*30, 30, 30))
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
