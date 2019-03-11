import pygame
from model.Player import *
from model.Deck import  *
from model.Hand import *
from model.Pot import *
from core.HandWinner import *
from enums.GameState import *

class PokerEngine:
    def __init__(self):
        self.roundsPlayed = 0
        playersPool = [ Player([], 1500, 0, "PLayer_unu"),
                         Player([], 1500, 1, "GigiKent"),
                         Player([], 1500, 2, "GGValuta"),
                         Player([], 1500, 3, "AmTalent"),
                         Player([], 1500, 4, "SefuLaBani"),
                         Player([], 1500, 5, "SerifIntergalactic"),
                         Player([], 1500, 6, "Bombardieru"),
                         Player([], 1500, 7, "Bo$$uLaPoker"),
                         Player([], 1500, 8, "DauGherle")]
        self.players = []
        for i in range(MAX_PLAYERS):
            self.players.append(playersPool[i])

        self.dealer = -1
        self.actingPlayer = -1
        self.firstToAct = -1
        self.blindIndex = 0
        self.state = GameState.InitRound
        self.waitingHumanInput = False

    def setGui(self, pokerGui):
        self.gui = pokerGui

    def initRound(self):
        self.deck = Deck()
        self.activePlayers = [0 for i in range(MAX_PLAYERS)]
        self.playersHands = [Hand([]) for i in range(MAX_PLAYERS)]
        self.activeBets = [0 for i in range(MAX_PLAYERS)]
        self.actedThisRound = [0 for i in range(MAX_PLAYERS)]
        self.money = [0 for i in range(MAX_PLAYERS)]
        for i in range(MAX_PLAYERS):
            self.players[i].holeCards = []

        # calculate the remaining players and deal them the hole cards
        for i in range(MAX_PLAYERS):
            if self.players[i].stack != 0:
                self.activePlayers[i] = 1

        self.blindIndex = int(self.roundsPlayed / HANDS_PER_ROUND)
        if self.blindIndex > len(BIG_BLINDS) - 1:
            self.blindIndex = len(BIG_BLINDS) - 1

        if ( self.dealer == -1 ):
            self.dealer = 0
        else:
            self.dealer = self.findNext(self.dealer)

        self.smallBlind = self.findNext(self.dealer)
        self.bigBlind = self.findNext(self.smallBlind)

        self.pots = []
        self.pots.append(Pot(0, self.activePlayers.copy()))

        self.communityCards = []
        self.flop = []
        self.turn = []
        self.river = []

    def findNext(self, index):
        length = len(self.activePlayers)
        for i in range(1, length):
            if self.activePlayers[(index + i) % length] == 1:
                return (index + i) % length

        # Everyone is all in or there is only one player left
        return -1

    def allEven(self):
        maximum = 0
        sidePots = []

        for i in range(len(self.activeBets)):
            if self.activeBets[i] > maximum and self.activePlayers[i] == 1:
                maximum = self.activeBets[i]
            if self.activePlayers[i] == 0.5:
                sidePots.append(self.activeBets[i])

        for i in range(len(self.activeBets)):
            if self.activePlayers[i]==1 and self.actedThisRound[i]==0:
                # The player didn't act yet
                return False
            if self.activeBets[i] != maximum and self.activePlayers[i] == 1:
                # The player bet but he still need to take call/fold/raise action
                return False
            elif len(sidePots) > 0 and self.activePlayers[i] == 1:
                for pot in sidePots:
                    if self.activeBets[i] < pot:
                        # This player can still call
                        return False

        return True

    def isRoundCompleted(self):
        if self.allEven():
            return True
        # if self.actingPlayer == self.firstToAct:
        #     return True
        if self.actingPlayer == -1:
            return True

    def getMaxBet(self):
        maxBet = 0
        for i in range(len(self.activeBets)):
            if self.activeBets[i] > maxBet:
                maxBet = self.activeBets[i]
        return maxBet

    def pre_flop_decision(self, agressionLevel, playerIndex, sumToCall):
        firstCard = self.players[playerIndex].holeCards[0]
        secondCard = self.players[playerIndex].holeCards[1]

        if firstCard.number==0:
            firstCard.number = 13
        if secondCard.number==0:
            secondCard.number = 13

        if firstCard.number<secondCard.number:
            aux = firstCard.number
            firstCard.number = secondCard.number
            secondCard.number = aux

        prob = 0
        if firstCard.suit==secondCard.suit:
            prob = HOLE_CARDS_PROBABILITIES[13 - firstCard.number][13 - secondCard.number]
        else:
            prob = HOLE_CARDS_PROBABILITIES[13 - firstCard.number][13 - secondCard.number]

        firstCard.number = firstCard.number%13
        secondCard.number = secondCard.number%13

        if agressionLevel==1:
            if prob>0.65:
                return min(3 * BIG_BLINDS[self.blindIndex], sumToCall, self.players[playerIndex].stack)
            else:
                return 0
        if agressionLevel==2:
            if prob>0.65:
                return min(3 * BIG_BLINDS[self.blindIndex], 3*sumToCall, self.players[playerIndex].stack)
            if prob>0.55:
                return min(sumToCall, self.players[playerIndex].stack)
            if prob<=0.55:
                return 0
        if agressionLevel==3:
            if prob>0.65:
                return min(3 * BIG_BLINDS[self.blindIndex], 3*sumToCall, self.players[playerIndex].stack)
            if prob>0.55:
                return 0
            if prob<=0.55:
                return min(3 * BIG_BLINDS[self.blindIndex], 3*sumToCall, self.players[playerIndex].stack)

    def decision(self, agressionLevel, playerIndex, sumToCall):
        howManyLeft = 5 - len(self.communityCards)
        ourHand = self.playersHands[playerIndex].compute_best_hand()
        powerLevel = Strength(ourHand)
        if sumToCall==0  and self.activeBets[playerIndex]==0:
            sumToCall = BIG_BLINDS[self.blindIndex] * len(self.communityCards)

        if agressionLevel==1:
            if powerLevel>=4 - howManyLeft:
                return sumToCall
            else:
                return 0
        if agressionLevel==2:
            if powerLevel>=5:
                return min(3*sumToCall, self.players[playerIndex].stack)
            if powerLevel>=3 - howManyLeft:
                return sumToCall
            else:
                return 0
        if agressionLevel==3:
            if powerLevel<3 - howManyLeft:
                return min(3*sumToCall, self.players[playerIndex].stack)
            if powerLevel>=5:
                return sumToCall
            if powerLevel>=3 - howManyLeft:
               return 0

    def takeActionAI(self):
        pygame.time.wait(30 + int(round(200)))

        playerToAct = self.actingPlayer
        if playerToAct==-1:
            return 0

        self.actedThisRound[playerToAct] = 1
        maxBet = self.getMaxBet()

        if len(self.communityCards)==0:
            new_bet = self.pre_flop_decision(random.randint(1,3), playerToAct, maxBet - self.activeBets[playerToAct])
            if new_bet>=maxBet - self.activeBets[playerToAct]:
                if self.players[playerToAct].stack > new_bet:
                    self.players[playerToAct].stack -= new_bet
                    self.activeBets[playerToAct] += new_bet
                else:
                    self.activeBets[playerToAct] += self.players[playerToAct].stack
                    self.players[playerToAct].stack = 0
                    self.activePlayers[playerToAct] = 0.5
            else:
                self.fold(playerToAct)
        else:
            new_bet = self.decision(random.randint(1, 3), playerToAct, maxBet - self.activeBets[playerToAct])
            if new_bet>=maxBet - self.activeBets[playerToAct]:
                if self.players[playerToAct].stack > new_bet:
                    self.players[playerToAct].stack -= new_bet
                    self.activeBets[playerToAct] += new_bet
                else:
                    self.activeBets[playerToAct] += self.players[playerToAct].stack
                    self.players[playerToAct].stack = 0
                    self.activePlayers[playerToAct] = 0.5
            else:
                self.fold(playerToAct)

        """if maxBet == 0:
            # amount = random.randint(min(BIG_BLINDS[self.blindIndex], self.players[playerToAct].stack),
            #                         self.players[playerToAct].stack)
            amount = min(0, BIG_BLINDS[self.blindIndex], self.players[playerToAct].stack)
            self.activeBets[playerToAct] = amount
            self.players[playerToAct].stack -= amount
        else:
            if self.activeBets[playerToAct] < maxBet:
                aux = random.randint(0, 1)
                if aux==0:
                    self.fold(playerToAct)
                if aux==1:
                    if self.players[playerToAct].stack > maxBet:
                        self.players[playerToAct].stack -= (maxBet - self.activeBets[playerToAct])
                        self.activeBets[playerToAct] = maxBet
                    else:
                        self.activeBets[playerToAct]+= self.players[playerToAct].stack
                        self.players[playerToAct].stack = 0
                        self.activePlayers[playerToAct] = 0.5"""

    def fold(self, index):
        self.activePlayers[index] = 0
        for pot in self.pots:
            pot.active_players[index] = 0

    def calculateRoundPot(self):
        maxBet = self.getMaxBet()
        self.actedThisRound = [0 for i in range(MAX_PLAYERS)]

        while True:
            noPots = len(self.pots)
            minBet = 1000000
            potThisRound = 0
            for i in range(len(self.pots[noPots - 1].active_players)):
                if self.pots[noPots - 1].active_players[i] == 1 and self.activeBets[i] < minBet:
                    minBet = self.activeBets[i]
                #if self.pots[noPots - 1].active_players[i]>0:
                potThisRound += self.activeBets[i]

            self.pots[noPots - 1].sum += potThisRound
            if minBet == maxBet:
                self.activeBets = [0 for i in range(MAX_PLAYERS)]
                break
            else:
                new_stack = 0
                new_ActivePlayers = [0 for i in range(MAX_PLAYERS)]
                for i in range(len(self.pots[noPots - 1].active_players)):
                    if self.pots[noPots - 1].active_players[i] == 1:
                        new_stack += (self.activeBets[i] - minBet)
                        self.pots[noPots - 1].sum -= (self.activeBets[i] - minBet)

                        if self.activeBets[i] != minBet:
                            new_ActivePlayers[i] = 1
                self.pots.append(Pot(new_stack, new_ActivePlayers))
