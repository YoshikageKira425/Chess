from src.pieces.piece import Piece
from src.pieces.pawn import Pawn
from src.pieces.knight import Knight
from src.pieces.rook import Rook
from src.pieces.bishop import Bishop
from src.pieces.queen import Queen
from src.pieces.king import King
from src.action import Action


class Board:
    def __init__(self):
        self.grid = [
            [Rook("bR"), Knight("bN"), Bishop("bB"), Queen("bQ"), King("bK"), Bishop("bB"), Knight("bN"), Rook("bR")],
            [Pawn("bP"), Pawn("bP"), Pawn("bP"), Pawn("bP"), Pawn("bP"), Pawn("bP"), Pawn("bP"), Pawn("bP")],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [Pawn("wP"), Pawn("wP"), Pawn("wP"), Pawn("wP"), Pawn("wP"), Pawn("wP"), Pawn("wP"), Pawn("wP")],
            [Rook("wR"), Knight("wN"), Bishop("wB"), Queen("wQ"), King("wK"), Bishop("wB"), Knight("wN"), Rook("wR")],
        ]
        
        self.white_king = self.grid[7][4]
        self.black_king = self.grid[0][4]
        
        self.actions: list[Action] = []

    def get(self, row: int, col: int) -> Piece | None:
        return self.grid[row][col]

    def move(self, from_pos: tuple, to_pos: tuple) -> Piece | None:
        """Moves a piece and returns the captured piece if any."""
        from_row, from_col = from_pos
        to_row, to_col = to_pos

        piece = self.grid[from_row][from_col]
        piece.set_indexes(to_row, to_col)
        
        captured = self.grid[to_row][to_col]

        self.grid[to_row][to_col] = piece
        self.grid[from_row][from_col] = None
        
        self.actions.append(Action(
            from_pos=from_pos,
            to_pos=to_pos,
            piece=piece,
            captured=captured
        ))

        return captured

    def is_valid_move(self, from_pos: tuple, to_pos: tuple) -> bool:
        from_row, from_col = from_pos
        piece = self.grid[from_row][from_col]

        if not piece:
            return False

        return piece.valid_move(self.grid, from_pos, to_pos)
    
    def undo(self) -> Action | None:
        if not self.actions:
            return None
        
        action = self.actions.pop()
        from_row, from_col = action.from_pos
        to_row, to_col = action.to_pos

        self.grid[from_row][from_col] = action.piece
        action.piece.set_indexes(from_row, from_col)
        
        self.grid[to_row][to_col] = action.captured
        
        return action

    def is_king_threatened(self, turn: bool) -> bool:
        enemy_color = "b" if turn else "w"
        king = self.white_king if turn else self.black_king
        
        for row in range(8):
            for col in range(8):
                piece = self.get(row, col)
                
                if piece is None:
                    continue
                
                if enemy_color == piece.color and piece.valid_move(self.grid, (row, col), king.get_indexes()):
                    return True
        
        return False

    def is_within_bounds(self, row: int, col: int) -> bool:
        return 0 <= row <= 7 and 0 <= col <= 7