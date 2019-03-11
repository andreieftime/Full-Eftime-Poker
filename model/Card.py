from enums.Suit import Suit
from enums.Number import Number

class Card:
    def __init__(self, suit, number):
        self.suit = suit
        self.number = number

        normalizedNumber = number + 1
        if normalizedNumber == 1:
            normalizedNumber = 14
        self.image_path = ('resources/images/deck/' + str(normalizedNumber) + Suit(self.suit).name[0] + '.png')

    def getDisplayName(self):
        return Number(self.number).name + " of " + Suit(self.suit).name;
