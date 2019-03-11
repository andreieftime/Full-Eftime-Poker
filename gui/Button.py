from constants import GuiConstants
import pygame

class Button:
    def __init__(self, parentSurface, font, text, callback, posX, posY, text2 = None):
        self.parentSurface = parentSurface
        self.text = font.render(text, 1, GuiConstants.WHITE)
        self.clickedCallback = callback
        self.posX = posX
        self.posY = posY
        self.text2 = text2

        self.isHovered = False
        self.isClicked = False
        self.background = pygame.image.load('resources/images/button.png')
        self.hoverBackground = pygame.image.load('resources/images/button-hover.png')
        self.clickBackground = pygame.image.load('resources/images/button-click.png')

        self.rect = self.background.get_rect(center=(posX + self.background.get_rect().width/2, posY + self.background.get_rect().height/2))
        self.parentSurface.blit(self.background.convert_alpha(), (self.posX, self.posY))

    def updateHovered(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.isHovered = True
        else:
            self.isHovered = False

    def draw(self):
        self.updateHovered()

        if self.isClicked:
            clickBackground = self.clickBackground.copy()
            if self.text2 != None:
                clickBackground.blit(self.text, (30, 5))
                clickBackground.blit(self.text2, (30, 25))
            else:
                clickBackground.blit(self.text, (30,20))
            self.parentSurface.blit(clickBackground.convert_alpha(), (self.posX, self.posY))

        elif self.isHovered:
            hoverBackground = self.hoverBackground.copy()
            if self.text2 != None:
                hoverBackground.blit(self.text, (30, 5))
                hoverBackground.blit(self.text2, (30, 25))
            else:
                hoverBackground.blit(self.text, (30, 20))
            self.parentSurface.blit(hoverBackground.convert_alpha(), (self.posX, self.posY))
        else:
            background = self.background.copy()
            if self.text2 != None:
                background.blit(self.text, (30, 5))
                background.blit(self.text2, (30, 25))
            else:
                background.blit(self.text, (30, 20))
            self.parentSurface.blit(background.convert_alpha(), (self.posX, self.posY))
