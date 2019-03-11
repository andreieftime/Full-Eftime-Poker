from enum import Enum, unique
@unique
class GameState(Enum):
    InitRound = -1
    BettingBlinds = 0
    DealingHoleCards = 1
    PreFlopBetting = 2
    DealingFlop = 3
    FlopBetting = 4
    DealingTurn = 5
    TurnBetting = 6
    DealingRiver = 7
    RiverBetting = 8
    Showdown = 9
    Idle = 10
    GameOver = 11
