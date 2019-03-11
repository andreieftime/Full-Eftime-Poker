import pygame
from constants.GuiConstants import *
from constants.GameConstants import *

class PlayerGui:
    def __init__(self, parentSurface, font, player ):
        self.parentSurface = parentSurface
        self.font = font
        self.player = player
        self.isActive = True
        self.showHand = True
        self.isCurrent = False
        self.showToggleBackground = False
        self.isWinner = False
        self.isHumanPlayer =  (player.index == HUMAN_PLAYER_INDEX)
        self.posX = PLAYER_COORDINATES_X[player.index]
        self.posY = PLAYER_COORDINATES_Y[player.index]

        if self.isHumanPlayer:
            self.surface =  pygame.Surface([161, 150], pygame.SRCALPHA, 32)
            self.cardSufrace = pygame.Surface([161, 116], pygame.SRCALPHA, 32)
        else:
            self.surface = pygame.Surface([161, 93], pygame.SRCALPHA, 32)
            self.cardSufrace = pygame.Surface([161, 70], pygame.SRCALPHA, 32)

        self.playerImage = pygame.image.load('resources/images/player-description-background.png')
        self.playerToggleImage = pygame.image.load('resources/images/player-description-background1.png')
        self.playerWinnerImage = pygame.image.load('resources/images/player-winner-background.png')

    def draw(self):
        surface = self.surface.copy()
        playerImage = self.playerImage.copy()
        cardSurface = self.cardSufrace.copy()

        if self.isCurrent :
            playerImage = self.playerToggleImage.copy()

        if self.isWinner :
            playerImage = self.playerWinnerImage.copy()

        if self.player.stack > 0 or self.isActive:
            playerNameText = self.font.render(self.player.name, 1, WHITE)
            playerStackText = self.font.render( str(self.player.stack), 1, WHITE)

            playerImage.blit(playerNameText, (25, 5))
            playerImage.blit(playerStackText, (35, playerImage.get_rect().height / 2))

            if len(self.player.holeCards) > 0 and self.isActive == True:
                if  self.isHumanPlayer == False and self.showHand == False:
                    cardImg = pygame.transform.smoothscale(pygame.image.load('resources/images/card-back.png').convert_alpha(),
                                                            (CARD_WITDH, CARD_HEIGHT))
                    cardSurface.blit(cardImg, (4, 0))
                    cardSurface.blit(cardImg, (67, 0))
                else:
                    cardImg = pygame.transform.smoothscale(
                        pygame.image.load(self.player.holeCards[0].image_path).convert_alpha(), (CARD_WITDH, CARD_HEIGHT))
                    cardSurface.blit(cardImg, (2, 0))
                    cardImg = pygame.transform.smoothscale(
                        pygame.image.load(self.player.holeCards[1].image_path).convert_alpha(), (CARD_WITDH, CARD_HEIGHT))
                    cardSurface.blit(cardImg, (67, 0))

            surface.blit(cardSurface.convert_alpha(), (0, 0))

            if self.isHumanPlayer:
                surface.blit(playerImage.convert_alpha(), (0,80))
            else:
                surface.blit(playerImage.convert_alpha(), (0, 40))
        else :
            surface.fill(pygame.Color(0,0,0,0))

        self.parentSurface.blit(surface.convert_alpha(), (self.posX, self.posY))
