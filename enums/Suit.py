from enum import Enum, unique
@unique
class Suit(Enum):
    """This is an enum representation of a card's suit"""
    Spades = 0
    Diamonds = 1
    Clubs = 2
    Hearts = 3