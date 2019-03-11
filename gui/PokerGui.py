import pygame, sys
from .BetSlider import *
from .Button import *
from .PlayerBetGui import *
from .PlayerGui import *
from .PotGui import *
from constants.GuiConstants import *
from constants.GameConstants import *
from enums.GameState import  *

class PokerGui:
    def __init__(self, surface, engine):
        self.surface = surface
        self.pokerEngine = engine
        self.backgroundImage = pygame.image.load('resources/images/background.jpg')
        self.tableImage = pygame.image.load('resources/images/table.png')
        self.playerControlsBackground = pygame.image.load('resources/images/player-controls-background.png')

        self.smallFont = pygame.font.SysFont("Verdana", 16, True)
        self.bigFont = pygame.font.SysFont("Verdana", 12, True)
        self.buttonFont = pygame.font.SysFont("Verdana", 16, False)
        self.betSlider = BetSlider(self.surface, self.smallFont, 200, 200, 2400, SCREEN_WIDTH - 300, SCREEN_HEIGHT - 125)
        self.potGui =  PotGui(self.surface, self.smallFont, 0, 550, 260)

        self.buttons = []
        self.playerBetGUIs = []
        self.playerGUIs = []

        for player in self.pokerEngine.players:
            playerGui = PlayerGui(self.surface, self.bigFont, player)

            if player.index == 2 or player.index == 3:
                playerBetGui = PlayerBetGui(self.surface, self.smallFont, player, allignRight=True)
            elif player.index == 7 or player.index == 8:
                playerBetGui = PlayerBetGui(self.surface, self.smallFont, player, allignLeft=True)
            else:
                playerBetGui = PlayerBetGui(self.surface, self.smallFont, player)

            self.playerGUIs.append(playerGui)
            self.playerBetGUIs.append(playerBetGui)

    def refreshData(self):
        for player in self.pokerEngine.players:
            for playerGui in self.playerGUIs:
                if player.index == playerGui.player.index:
                    playerGui.isActive = self.pokerEngine.activePlayers[player.index]
                    playerGui.isCurrent = (self.pokerEngine.actingPlayer == player.index)
                    playerGui.isWinner = False
                    if self.pokerEngine.state == GameState.Idle:
                        if self.pokerEngine.money[player.index] > 0:
                            playerGui.isWinner = True
                        break

            for playerBetGui in self.playerBetGUIs:
                if player.index == playerBetGui.player.index:
                    playerBetGui.betValue = self.pokerEngine.activeBets[player.index]
                    playerBetGui.isDealer = (playerBetGui.player.index == self.pokerEngine.dealer)
                    break

        potValue = 0
        for pot in self.pokerEngine.pots:
            potValue += pot.sum
        self.potGui.potValue = potValue

        if self.pokerEngine.state == GameState.Idle or self.pokerEngine.state == GameState.Showdown:
            for playerGui in self.playerGUIs:
                playerGui.showHand = True
        else:
            for playerGui in self.playerGUIs:
                playerGui.showHand = False

    def drawCommunityCards(self):
        index = 0
        startX = ((SCREEN_WIDTH - self.tableImage.get_rect().width) / 2) + \
                 (self.tableImage.get_rect().width - 5 * CARD_WITDH - 4 * 5) / 2
        startY = (SCREEN_HEIGHT - self.tableImage.get_rect().height) / 2 + \
                 (self.tableImage.get_rect().height - CARD_HEIGHT) / 2 + 20
        for card in self.pokerEngine.communityCards:
            cardImg = pygame.transform.smoothscale(pygame.image.load(card.image_path).convert_alpha(),
                                                   (CARD_WITDH, CARD_HEIGHT))
            self.surface.blit(cardImg, (startX + index * (CARD_WITDH + 5), startY))
            index = index + 1

    def draw(self, shouldRefreshGameData = False):
        if shouldRefreshGameData:
            self.refreshData()

            surface = self.surface
            backgroundImage = self.backgroundImage.copy()
            tableImage = self.tableImage.copy()

            surface.blit(backgroundImage.convert_alpha(), (0, 0))

            # Center the table based on the screen size and the table image size
            tableLocation = ((SCREEN_WIDTH - tableImage.get_rect().width) / 2,
                             (SCREEN_HEIGHT - tableImage.get_rect().height) / 2)

            surface.blit(tableImage.convert_alpha(), tableLocation)

            self.drawCommunityCards()

            for playerGui in self.playerGUIs:
                playerGui.draw()
            for playerBet in self.playerBetGUIs:
                playerBet.draw()

            self.potGui.draw()

        if self.pokerEngine.waitingHumanInput:
            if shouldRefreshGameData:
                maxBet = self.pokerEngine.getMaxBet()
                if (maxBet > 0):
                    self.betSlider.betValue = maxBet
                    self.betSlider.minValue = maxBet
                    self.betSlider.maxValue = self.pokerEngine.players[HUMAN_PLAYER_INDEX].stack

                    self.buttons = [
                        Button(self.surface, self.buttonFont, "Fold", None, SCREEN_WIDTH - 400, SCREEN_HEIGHT - 80),
                        Button(self.surface, self.buttonFont, "Call " + str(maxBet), None, SCREEN_WIDTH - 270,
                               SCREEN_HEIGHT - 80),
                        Button(self.surface, self.buttonFont, "Raise to", None, SCREEN_WIDTH - 140,
                               SCREEN_HEIGHT - 80, self.buttonFont.render(str(2 * maxBet), 1, GuiConstants.WHITE))
                        ]
                else:
                    self.betSlider.betValue = BIG_BLINDS[self.pokerEngine.blindIndex]
                    self.betSlider.minValue = BIG_BLINDS[self.pokerEngine.blindIndex]
                    self.betSlider.maxValue = self.pokerEngine.players[HUMAN_PLAYER_INDEX].stack

                    self.buttons = [
                        Button(self.surface, self.buttonFont, "Check", None, SCREEN_WIDTH - 270, SCREEN_HEIGHT - 80),
                        Button(self.surface, self.buttonFont, "Bet", None, SCREEN_WIDTH - 140,
                               SCREEN_HEIGHT - 80)
                        ]

                playerControlsBackground = self.playerControlsBackground.copy()
                surface.blit(playerControlsBackground, (SCREEN_WIDTH - 430, SCREEN_HEIGHT - 130))

            self.betSlider.draw()
            if len(self.buttons) == 3:
                self.buttons[2].text2 = self.buttonFont.render(str ( int(self.betSlider.betValue) ), 1, GuiConstants.WHITE)
            if len(self.buttons) == 2:
                self.buttons[1].text2 = self.buttonFont.render(str(int(self.betSlider.betValue)), 1, GuiConstants.WHITE)

            for button in self.buttons:
                button.draw()
