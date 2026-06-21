from src.pieces.piece import Piece
from src.pieces.pawn import Pawn
from src.pieces.knight import Knight
from src.pieces.rook import Rook
from src.pieces.bishop import Bishop
from src.pieces.queen import Queen


class Board:
    def __init__(self):
        self.grid = [
            [Rook("bR"), Knight("bN"), Bishop("bB"), Queen("bQ"), Piece("bK"), Bishop("bB"), Knight("bN"), Rook("bR")],
            [Pawn("bP"), Pawn("bP"), Pawn("bP"), Pawn("bP"), Pawn("bP"), Pawn("bP"), Pawn("bP"), Pawn("bP")],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [Pawn("wP"), Pawn("wP"), None, None, None, Pawn("wP"), Pawn("wP"), Pawn("wP")],
            [Rook("wR"), Knight("wN"), Bishop("wB"), Queen("wQ"), Piece("wK"), Bishop("wB"), Knight("wN"), Rook("wR")],
        ]

    def get(self, row: int, col: int) -> Piece | None:
        return self.grid[row][col]

    def move(self, from_pos: tuple, to_pos: tuple) -> Piece | None:
        """Moves a piece and returns the captured piece if any."""
        from_row, from_col = from_pos
        to_row, to_col = to_pos

        piece = self.grid[from_row][from_col]
        captured = self.grid[to_row][to_col]

        self.grid[to_row][to_col] = piece
        self.grid[from_row][from_col] = None

        return captured

    def is_valid_move(self, from_pos: tuple, to_pos: tuple) -> bool:
        from_row, from_col = from_pos
        piece = self.grid[from_row][from_col]

        if not piece:
            return False

        return piece.valid_move(self.grid, from_pos, to_pos)

    def is_within_bounds(self, row: int, col: int) -> bool:
        return 0 <= row <= 7 and 0 <= col <= 7