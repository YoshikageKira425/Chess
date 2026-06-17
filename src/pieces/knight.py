from .piece import Piece

class Knight(Piece):
    def __init__(self, piece):
        super().__init__(piece)
        
    def valid_move(self, board: list[list[Piece]], from_pos: tuple, to_pos: tuple) -> bool:
        from_row, from_col = from_pos
        
        possible_moves = [(from_row + 1, from_col + 2), (from_row - 1, from_col + 2), (from_row + 2, from_col + 1), 
                          (from_row + 2, from_col - 1), (from_row - 2, from_col + 1), (from_row - 2, from_col - 1), 
                          (from_row + 1, from_col - 2), (from_row - 1, from_col - 2)]
        
        return to_pos in possible_moves