import pygame
from constants import GuiConstants

class BetSlider():
    def __init__(self, surface, font, startValue, minValue, maxValue, posX, posY):
        self.betValue = startValue
        self.minValue = minValue
        self.maxValue = maxValue
        self.posX = posX
        self.posY = posY
        self.hit = False
        self.surface = surface
        self.font = font
        self.backgroundImage = pygame.image.load('resources/images/bet-slider.png')
        self.slideButtonImage = pygame.image.load('resources/images/bet-slide-button.png')
        self.betAmountImage = pygame.image.load('resources/images/bet-amount-background.png')


    def draw(self):
        surfaceCopy = self.backgroundImage.copy()

        pos = (18 + int((self.betValue-self.minValue)/(self.maxValue-self.minValue)*215), 18)

        self.buttonRect = self.slideButtonImage.get_rect(center=pos)
        surfaceCopy.blit(self.slideButtonImage.convert_alpha(), self.buttonRect )
        self.buttonRect.move_ip((self.posX, self.posY))
        self.surface.blit(surfaceCopy.convert_alpha(), (self.posX, self.posY))

        surfaceCopy = self.betAmountImage.copy()
        self.betText = self.font.render(str(int(self.betValue)), 1, GuiConstants.WHITE)
        surfaceCopy.blit(self.betText.convert_alpha(), self.betText.get_rect(center=(30, 15)))
        self.surface.blit(surfaceCopy, (self.posX - self.betAmountImage.get_rect().width - 5, self.posY))

    def move(self):
        self.betValue = (pygame.mouse.get_pos()[0] - self.posX - 18) / 215 * (self.maxValue - self.minValue) + self.minValue
        if self.betValue < self.minValue:
            self.betValue = self.minValue
        if self.betValue > self.maxValue:
            self.betValue = self.maxValue