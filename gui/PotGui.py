import pygame
from constants import GuiConstants


class PotGui:
    def __init__(self, parentSurface, font, potValue, posX, posY):
        self.parentSurface = parentSurface
        self.font = font
        self.potValue = potValue
        self.posX = posX
        self.posY = posY
        self.potImage = pygame.image.load('resources/images/pot.png')
        self.surface = pygame.Surface([210, 50], pygame.SRCALPHA, 32)

    def draw(self):
        surface = self.surface.copy()

        if self.potValue > 0 :
            potText = self.font.render(str(self.potValue), 1, GuiConstants.WHITE)
            surface.blit(self.potImage.convert_alpha(), (0, 0))
            surface.blit(potText, (150, 10))

        self.parentSurface.blit(surface, (self.posX, self.posY))

