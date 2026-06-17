from .piece import Piece

class Pawn(Piece):
    def __init__(self, piece):
        super().__init__(piece)
        
        self.is_first_move = True
        
    def valid_move(self, board: list[list[Piece]], from_pos: tuple, to_pos: tuple) -> bool:
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        if from_row == to_row or from_col != to_col:
            return False
        
        one_step = 1 if self.color == "w" else -1
        two_step = 2 if self.color == "w" else -2
        
        return (to_row + one_step == from_row) or (to_row + two_step == from_row and self.is_first_move)
    
    def pieced_moved(self):
        self.is_first_move = False