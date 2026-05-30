import arcade
from .game_visual import GameVisual
from .pieces.piece import Piece


class GameView(arcade.View):
    def __init__(self):
        super().__init__()

        self.board = [
            [Piece("bR"), Piece("bN"), Piece("bB"), Piece("bQ"), Piece("bK"), Piece("bB"), Piece("bN"), Piece("bR")],
            [Piece("bP"), Piece("bP"), Piece("bP"), Piece("bP"),Piece("bP"), Piece("bP"), Piece("bP"), Piece("bP")],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [Piece("wP"), Piece("wP"), Piece("wP"), Piece("wP"), Piece("wP"), Piece("wP"), Piece("wP"), Piece("wP")],
            [Piece("wR"), Piece("wN"), Piece("wB"), Piece("wQ"), Piece("wK"), Piece("wB"), Piece("wN"), Piece("wR")],
        ]
        
        self.visual = GameVisual(self.board)

    def on_draw(self):
        self.clear()
        self.visual.draw()
