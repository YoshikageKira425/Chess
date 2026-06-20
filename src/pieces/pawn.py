from .piece import Piece
from ..constants import HIGHLIGHT_MOVE, HIGHLIGHT_CAPTURE

class Pawn(Piece):
    def __init__(self, piece):
        super().__init__(piece)
        
        self.is_first_move = True
        
    def valid_move(self, board: list[list[Piece]], from_pos: tuple, to_pos: tuple) -> bool:
        from_row, from_col = from_pos
        to_row, to_col = to_pos

        direction = -1 if self.color == "w" else 1

        if (
            to_col == from_col
            and to_row == from_row + direction
            and board[to_row][to_col] is None
        ):
            return True

        if (
            self.is_first_move
            and to_col == from_col
            and to_row == from_row + direction * 2
            and board[from_row + direction][from_col] is None
            and board[to_row][to_col] is None
        ):
            return True

        if (
            abs(to_col - from_col) == 1
            and to_row == from_row + direction
        ):
            target = board[to_row][to_col]

            if target is not None and target.color != self.color:
                return True

        return False
    
    def move_hightlight(self, board: list[list[Piece]], from_pos: tuple) -> list[tuple]:
        from_row, from_col = from_pos
        highlights = []
        
        direction = -1 if self.color == "w" else 1
        
        row = from_row + direction
        col = from_col - 1

        if (
            0 <= row < 8
            and 0 <= col < 8
            and board[row][col] is not None
            and board[row][col].color != self.color
        ):
            highlights.append((row, col, HIGHLIGHT_CAPTURE))

        col = from_col + 1

        if (
            0 <= row < 8
            and 0 <= col < 8
            and board[row][col] is not None
            and board[row][col].color != self.color
        ):
            highlights.append((row, col, HIGHLIGHT_CAPTURE))
        
        if board[from_row + direction][from_col] is None:
            highlights.append((from_row + direction, from_col, HIGHLIGHT_MOVE))
        else:
            return highlights
        
        if self.is_first_move and board[from_row + direction * 2][from_col] is None:
            highlights.append((from_row + direction * 2, from_col, HIGHLIGHT_MOVE))
        
        return highlights
    
    def pieced_moved(self):
        self.is_first_move = False