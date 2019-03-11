import os
from gui.PokerGui import *
from core.PokerEngine import *
import threading
from enums.GameState import *


if __name__=="__main__":

    os.environ['SDL_VIDEO_CENTERED'] = '1'  # center screen
    pygame.init()
    screen = pygame.display.set_mode((GuiConstants.SCREEN_WIDTH, GuiConstants.SCREEN_HEIGHT), 0, 32)

    pygame.display.set_caption("FullEftimePoker")
    engine = PokerEngine()

    pokerGui = PokerGui(screen, engine)

    # thread2 = threading.Thread(target=engine.play())
    # thread2.start()

    while True:
        shouldRefreshGameData = False

        if engine.waitingHumanInput == True:
            engine.actedThisRound[HUMAN_PLAYER_INDEX] = 1
            if len(pokerGui.buttons) == 2:
                if pokerGui.buttons[0].isClicked == True:
                    # Check
                    engine.waitingHumanInput = False
                    engine.actingPlayer = engine.findNext(engine.actingPlayer)
                    shouldRefreshGameData = True
                if pokerGui.buttons[1].isClicked == True:
                    # Raise
                    engine.activeBets[HUMAN_PLAYER_INDEX] = int(pokerGui.betSlider.betValue)
                    engine.players[HUMAN_PLAYER_INDEX].stack -= int(pokerGui.betSlider.betValue)
                    engine.waitingHumanInput = False
                    engine.actingPlayer = engine.findNext(engine.actingPlayer)
                    shouldRefreshGameData = True
            elif len(pokerGui.buttons) == 3:
                if pokerGui.buttons[0].isClicked == True:
                    # Fold
                    engine.activePlayers[HUMAN_PLAYER_INDEX] = 0
                    for pot in engine.pots:
                        pot.active_players[HUMAN_PLAYER_INDEX] = 0
                    engine.waitingHumanInput = False
                    engine.actingPlayer = engine.findNext(engine.actingPlayer)
                    shouldRefreshGameData = True
                if pokerGui.buttons[1].isClicked == True:
                    # Call
                    engine.players[HUMAN_PLAYER_INDEX].stack -= min(engine.players[HUMAN_PLAYER_INDEX].stack,engine.getMaxBet() - engine.activeBets[HUMAN_PLAYER_INDEX])
                    engine.activeBets[HUMAN_PLAYER_INDEX] = engine.getMaxBet()
                    if engine.players[HUMAN_PLAYER_INDEX].stack == 0:
                        # All In
                        engine.activePlayers[HUMAN_PLAYER_INDEX] = 0.5
                    engine.waitingHumanInput = False
                    engine.actingPlayer = engine.findNext(engine.actingPlayer)
                    shouldRefreshGameData = True
                if pokerGui.buttons[2].isClicked == True:
                    # Raise
                    engine.activeBets[HUMAN_PLAYER_INDEX] = int(pokerGui.betSlider.betValue)
                    engine.players[HUMAN_PLAYER_INDEX].stack -= int(pokerGui.betSlider.betValue)
                    if engine.players[HUMAN_PLAYER_INDEX].stack == 0:
                        # All In
                        engine.activePlayers[HUMAN_PLAYER_INDEX] = 0.5
                    engine.waitingHumanInput = False
                    engine.actingPlayer = engine.findNext(engine.actingPlayer)
                    shouldRefreshGameData = True
            # Force the UI refresh after every button click
            for button in pokerGui.buttons:
                if button.isClicked:
                    pokerGui.draw(shouldRefreshGameData)
                    pygame.display.update()
                    break

        if engine.state == GameState.InitRound:
            remainingPlayers = 0
            for player in engine.players:
                if player.stack > 0:
                    remainingPlayers += 1

            if remainingPlayers <= 1:
                engine.state = GameState.GameOver
            else:
                engine.initRound()
                engine.state = GameState.BettingBlinds

                shouldRefreshGameData = True
                pygame.time.wait(200)
        elif engine.state == GameState.BettingBlinds:
            if engine.activeBets[engine.smallBlind] == 0:
                engine.activeBets[engine.smallBlind] = BIG_BLINDS[engine.blindIndex] // 2
                engine.players[engine.smallBlind].stack -= BIG_BLINDS[engine.blindIndex] // 2
            else:
                engine.activeBets[engine.bigBlind] = BIG_BLINDS[engine.blindIndex]
                engine.players[engine.bigBlind].stack -= BIG_BLINDS[engine.blindIndex]

                engine.state = GameState.DealingHoleCards

            shouldRefreshGameData = True
            pygame.time.wait(200)

        elif engine.state == GameState.DealingHoleCards:
            # Deal cards to each active player at the time
            i = engine.findNext(engine.dealer)
            while engine.players[i].stack > 0 and \
                    len(engine.players[i].holeCards) > 0:
                i = engine.findNext(i)

            engine.activePlayers[i] = 1
            engine.players[i].holeCards = [engine.deck.draw(), engine.deck.draw()]
            engine.playersHands[i] = Hand(engine.players[i].holeCards)

            # Check if everyone got their hole cards:
            if i == engine.dealer:
                engine.actingPlayer = engine.findNext( engine.bigBlind)
                engine.firstToAct = engine.findNext(engine.bigBlind)
                engine.state = GameState.PreFlopBetting

            shouldRefreshGameData = True
            pygame.time.wait(50)

        elif engine.state == GameState.PreFlopBetting:
            if engine.actingPlayer == -1:
                engine.state = GameState.DealingFlop
                pygame.time.wait(200)

            if engine.actingPlayer != HUMAN_PLAYER_INDEX:
                engine.takeActionAI()
                engine.actingPlayer = engine.findNext(engine.actingPlayer)
                if engine.isRoundCompleted():
                    engine.calculateRoundPot()
                    engine.state = GameState.DealingFlop

                shouldRefreshGameData = True
                pygame.time.wait(200)
            else:
                if engine.players[HUMAN_PLAYER_INDEX].stack > 0:
                    if engine.waitingHumanInput == False:
                        shouldRefreshGameData = True
                    engine.waitingHumanInput = True
                else:
                    engine.actingPlayer = engine.findNext(engine.actingPlayer)

        elif engine.state == GameState.DealingFlop:
            card = engine.deck.draw()
            engine.flop.append(card)
            engine.communityCards.append(card)
            for i in range(MAX_PLAYERS):
                if engine.activePlayers[i] > 0:
                    engine.playersHands[i].cards.append(card)

            if len(engine.flop) == 3:
                engine.actingPlayer = engine.findNext(engine.dealer)
                engine.firstToAct = engine.findNext(engine.dealer)
                engine.state = GameState.FlopBetting

            shouldRefreshGameData = True
            pygame.time.wait(500)

        elif engine.state == GameState.FlopBetting:
            if engine.actingPlayer == -1:
                engine.state = GameState.DealingTurn
                pygame.time.wait(200)

            if engine.actingPlayer != HUMAN_PLAYER_INDEX:
                engine.takeActionAI()
                engine.actingPlayer = engine.findNext(engine.actingPlayer)

                if engine.isRoundCompleted():
                    engine.calculateRoundPot()
                    engine.state = GameState.DealingTurn

                shouldRefreshGameData = True
                pygame.time.wait(200)
            else:
                if engine.players[HUMAN_PLAYER_INDEX].stack > 0:
                    if engine.waitingHumanInput == False:
                        shouldRefreshGameData = True
                    engine.waitingHumanInput = True
                else:
                    engine.actingPlayer = engine.findNext(engine.actingPlayer)


        elif engine.state == GameState.DealingTurn:
            card = engine.deck.draw()
            engine.turn.append(card)
            engine.communityCards.append(card)
            for i in range(MAX_PLAYERS):
                if engine.activePlayers[i] > 0:
                    engine.playersHands[i].cards.append(card)

            engine.actingPlayer = engine.findNext(engine.dealer)
            engine.firstToAct = engine.findNext(engine.dealer)
            engine.state = GameState.TurnBetting

            shouldRefreshGameData = True
            pygame.time.wait(500)

        elif engine.state == GameState.TurnBetting:
            if engine.actingPlayer == -1:
                engine.state = GameState.DealingRiver
                pygame.time.wait(200)

            if engine.actingPlayer != HUMAN_PLAYER_INDEX:
                engine.takeActionAI()
                engine.actingPlayer = engine.findNext(engine.actingPlayer)

                if engine.isRoundCompleted():
                    engine.calculateRoundPot()
                    engine.state = GameState.DealingRiver

                shouldRefreshGameData = True
                pygame.time.wait(200)
            else:
                if engine.players[HUMAN_PLAYER_INDEX].stack > 0:
                    if engine.waitingHumanInput == False:
                        shouldRefreshGameData = True
                    engine.waitingHumanInput = True
                else:
                    engine.actingPlayer = engine.findNext(engine.actingPlayer)

        elif engine.state == GameState.DealingRiver:
            if engine.actingPlayer == -1:
                engine.state = GameState.Showdown
                pygame.time.wait(200)

            card = engine.deck.draw()
            engine.turn.append(card)
            engine.communityCards.append(card)
            for i in range(MAX_PLAYERS):
                if engine.activePlayers[i] > 0:
                    engine.playersHands[i].cards.append(card)

            engine.actingPlayer = engine.findNext(engine.dealer)
            engine.firstToAct = engine.findNext(engine.dealer)
            engine.state = GameState.RiverBetting

            shouldRefreshGameData = True
            pygame.time.wait(500)

        elif engine.state == GameState.RiverBetting:
            if engine.actingPlayer == -1:
                engine.state = GameState.DealingFlop
                pygame.time.wait(200)

            if engine.actingPlayer != HUMAN_PLAYER_INDEX:
                engine.takeActionAI()
                engine.actingPlayer = engine.findNext(engine.actingPlayer)

                if engine.isRoundCompleted():
                    engine.calculateRoundPot()
                    engine.state = GameState.Showdown

                shouldRefreshGameData = True
                pygame.time.wait(200)
            else:
                if engine.players[HUMAN_PLAYER_INDEX].stack > 0:
                    if engine.waitingHumanInput == False:
                        shouldRefreshGameData = True
                    engine.waitingHumanInput = True
                else:
                    engine.actingPlayer = engine.findNext(engine.actingPlayer)

        elif engine.state == GameState.Showdown:
            finalHands = []
            for i in range(MAX_PLAYERS):
                finalHands.append(engine.playersHands[i].compute_best_hand())

            engine.money = feud(finalHands, engine.pots)
            for i in range(MAX_PLAYERS):
                engine.players[i].stack += int(engine.money[i])

            engine.roundsPlayed += 1
            shouldRefreshGameData = True
            engine.state = GameState.Idle

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONUP and engine.state == GameState.Idle :
                engine.state = GameState.InitRound

            if ( engine.waitingHumanInput == True ):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if pokerGui.betSlider.buttonRect.collidepoint(pos):
                        pokerGui.betSlider.hit = True
                    for button in pokerGui.buttons:
                        if button.rect.collidepoint(pos):
                            button.isClicked = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    pokerGui.betSlider.hit = False
                    for button in pokerGui.buttons:
                        button.isClicked = False

                if pokerGui.betSlider.hit:
                    pokerGui.betSlider.move()

        pokerGui.draw(shouldRefreshGameData)
        pygame.display.update()
        pygame.time.Clock().tick(120)


