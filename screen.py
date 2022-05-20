import pygame
pygame.init()
background_colour = (0, 0, 0)
(width, height) = (800, 600)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('UV Chess')
screen.fill(background_colour)
pygame.display.flip()
running = True


class Tile:
    def __init__(self, xPos, yPos):
        self.x = xPos
        self.y = yPos

    def draw(self, screen):
        surface = screen
        pygame.draw.rect(surface, (255, 0, 0), pygame.Rect(30, 30, 60, 60))
        pygame.display.flip()


while running:
    square = Tile(0, 0)
    square.draw(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
