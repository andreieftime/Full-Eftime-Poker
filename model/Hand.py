from core.HandStrength import *
from model.Card import *

class Hand:
    def __init__(self, cards):
        self.cards = cards

    def compute_best_hand(self):
        if len(self.cards)==5:
            return self.cards
        if len(self.cards)==6:
            best_hand = [Card(1 // 13, 1 % 13),
                         Card(2 // 13, 2 % 13),
                         Card(3 // 13, 3 % 13),
                         Card(4 // 13, 4 % 13),
                         Card(19 // 13, 19 % 13)]
            for i in range(6):
                new_contender =[]
                for j in range(6):
                    if j!=i:
                        new_contender.append(self.cards[j])
                if HandCompare(new_contender, best_hand)==1:
                    best_hand = new_contender

            return best_hand

        if len(self.cards)==7:
            best_hand = [Card(1 // 13, 1 % 13),
                         Card(2 // 13, 2 % 13),
                         Card(3 // 13, 3 % 13),
                         Card(4 // 13, 4 % 13),
                         Card(19 // 13, 19 % 13)]
            for i in range(7):
                for h in range(7):
                    if h!=i:
                        new_contender = []
                        for j in range(7):
                            if j != i and j != h:
                                new_contender.append(self.cards[j])
                        if HandCompare(new_contender, best_hand) == 1:
                            best_hand = new_contender

            return best_hand