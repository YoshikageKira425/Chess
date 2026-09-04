from enum import Enum

class GameStatus(Enum):
    ON_GOING = "on_going"
    WHITE_WON = "white_won"
    BLACK_WON = "black_won"
    DRAW = "draw"