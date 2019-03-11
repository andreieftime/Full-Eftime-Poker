import random
from model.Card import Card
from enums.Suit import  Suit

class Deck:

    def __init__(self):
        self.cards = [i for i in range(52)]
        random.shuffle(self.cards)
        self.currentCardIndex = 0

    def draw(self):
        currentSuit = self.cards[self.currentCardIndex] // 13
        currentNumber = self.cards[self.currentCardIndex] % 13
        self.currentCardIndex += 1

        return Card(currentSuit, currentNumber)
