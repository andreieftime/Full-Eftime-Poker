import pygame
from constants.GuiConstants import *

class PlayerBetGui:
    def __init__(self, parentSurface, font, player, isDealer = False, betValue = 0, allignLeft=False, allignRight=False):
        self.parentSurface = parentSurface
        self.font = font
        self.player = player
        self.isDealer = isDealer
        self.betValue = betValue
        self.allignLeft = allignLeft
        self.allignRight = allignRight
        self.posX = BETS_COORDINATES_X[player.index]
        self.posY = BETS_COORDINATES_Y[player.index]
        self.chipsImage = pygame.image.load('resources/images/player-bet.png')
        self.dealerBtnImage = pygame.image.load('resources/images/dealer-button.png')

        if self.allignLeft or self.allignRight:
            self.surface = pygame.Surface([115, 100], pygame.SRCALPHA, 32)
        else:
            self.surface = pygame.Surface([170, 55], pygame.SRCALPHA, 32)

    def draw(self):
        surface = self.surface.copy()
        surface.fill(pygame.Color(0, 0, 0, 0))

        if self.isDealer:
            if self.allignRight:
                surface.blit(self.dealerBtnImage.convert_alpha(), (70, 45))
            elif self.allignLeft:
                surface.blit(self.dealerBtnImage.convert_alpha(), (0, 45))
            else:
                surface.blit(self.dealerBtnImage.convert_alpha(), (0,10))

        if self.betValue > 0:
            betText = self.font.render(str(self.betValue), 1, WHITE)

            if self.allignRight:
                surface.blit(self.chipsImage.convert_alpha(), (0, 0))
                surface.blit(betText, (60, 10))
            elif self.allignLeft:
                surface.blit(self.chipsImage.convert_alpha(), (0, 0))
                surface.blit(betText, (60, 10))
            else:
                surface.blit(self.chipsImage.convert_alpha(), (50, 0))
                surface.blit(betText, (110, 10))

        self.parentSurface.blit(surface, (self.posX, self.posY))
