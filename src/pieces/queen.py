from .piece import Piece
from .sliding_logic import diagonal_path_clear, straight_path_clear, generate_highlight_lines

class Queen(Piece):
    def __init__(self, piece):
        super().__init__(piece)

    def valid_move(self, board: list[list[Piece]], from_pos: tuple, to_pos: tuple, last_action=None) -> bool: 
        if not straight_path_clear(board, from_pos, to_pos) and not diagonal_path_clear(board, from_pos, to_pos):
            return False
        
        to_row, to_col = to_pos
        target = board[to_row][to_col]

        return target is None or target.color != self.color
    
    def move_highlight(self, board: list[list[Piece]], from_pos: tuple, last_action=None) -> list[tuple]:
        directions = [
            (1, 0),   # down
            (-1, 0),  # up
            (0, 1),   # right
            (0, -1),  # left
            (1, 1),   # right-top
            (-1, -1),  # right-down
            (-1, 1),   # left-top
            (1, -1),  # left-down
        ]
        
        return generate_highlight_lines(directions, self.color, from_pos, board)