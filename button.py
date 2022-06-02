import pygame
import handler as HANDLER

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False

    def buttonTick(self):
        #get mouse pos
        pos = HANDLER.getMousePos()
        print(pos)
        print(self.rect)

        #check if mousing over button or clicked button
        if self.rect.collidepoint(pos):
            print("Mouse on button")
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False


    def buttonRender(self, surface):
        #drawing to screen
        surface.blit(self.image, (self.rect.x, self.rect.y))

    def getClicked(self):
        return self.clicked
