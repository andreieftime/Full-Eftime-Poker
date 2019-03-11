from enum import Enum, unique
@unique
class Number(Enum):
    """This is an enum representation of a card's number or symbol"""
    Ace = 0
    Two = 1
    Three = 2
    Four = 3
    Five = 4
    Six = 5
    Seven = 6
    Eight = 7
    Nine = 8
    Ten = 9
    Jack = 10
    Queen = 11
    King = 12
    As = 13