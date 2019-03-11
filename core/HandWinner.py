from core.HandStrength import *
from model.Card import *
from constants.GameConstants import *


#we will use this function to settle how much money is
#each player going to get from the pot(or pots) in the case
#of chops or side pots
def feud(hands, pots):
    #the function will return a vector with the values that have to be added to each
    #player's stack
    winnings = [0 for i in range(MAX_PLAYERS)]

    for pot in pots:
        act_sum = pot.sum

        #we want to establish who has the best hand for this pot
        best_hand = [Card(1//13, 1%13),
                     Card(2//13, 2%13),
                     Card(3//13, 3%13),
                     Card(4//13, 4%13),
                     Card(19//13, 19%13)]

        #we initialize it with the worst possible hand
        for i in range(len(pot.active_players)):
            if pot.active_players[i] == 1 and HandCompare(hands[i], best_hand) == 1:
                best_hand = hands[i]

        #we decide in how many ways we should split the pot
        winners = 0
        for i in range(len(pot.active_players)):
            if pot.active_players[i] == 1 and HandCompare(hands[i], best_hand) == -1:
                winners += 1

        #then we give each player what he deserves
        for i in range(len(pot.active_players)):
            if pot.active_players[i] == 1 and HandCompare(hands[i], best_hand) == -1:
                winnings[i] += act_sum / winners

    return winnings