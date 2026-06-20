from .piece import Piece
from ..constants import HIGHLIGHT_MOVE, HIGHLIGHT_CAPTURE

class Bishop(Piece):
    def __init__(self, piece):
        super().__init__(piece)

    def valid_move(self, board: list[list[Piece]], from_pos: tuple, to_pos: tuple) -> bool:
        from_row, from_col = from_pos
        to_row, to_col = to_pos

        if abs(to_row - from_row) != abs(to_col - from_col):
            return False
        
        row_step = 1 if from_row < to_row else -1
        col_step = 1 if from_col < to_col else -1

        cur_row, cur_col = from_row + row_step, from_col + col_step
        while (cur_row, cur_col) != (to_row, to_col):
            if board[cur_row][cur_col] is not None:
                return False
            
            cur_row += row_step
            cur_col += col_step

        target = board[to_row][to_col]
        if target is not None and target.color == self.color:
            return False

        return True
    
    def move_hightlight(self, board: list[list[Piece]], from_pos: tuple) -> list[tuple]:
        from_row, from_col = from_pos
        highlights = []

        directions = [
            (1, 1),   # right-top
            (-1, -1),  # right-down
            (-1, 1),   # left-top
            (1, -1),  # left-down
        ]

        for dr, dc in directions:
            row = from_row + dr
            col = from_col + dc

            while 0 <= row < 8 and 0 <= col < 8:
                piece = board[row][col]

                if piece is None:
                    highlights.append((row, col, HIGHLIGHT_MOVE))
                elif piece.color != self.color:
                    highlights.append((row, col, HIGHLIGHT_CAPTURE))
                    break
                else:
                    break

                row += dr
                col += dc

        return highlights