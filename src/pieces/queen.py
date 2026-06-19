from .piece import Piece

class Queen(Piece):
    def __init__(self, piece):
        super().__init__(piece)

    def valid_move(self, board: list[list[Piece]], from_pos: tuple, to_pos: tuple) -> bool: 
        if not self.rook_behavior(board, from_pos, to_pos) and not self.bishop_behavior(board, from_pos, to_pos):
            return False
        
        to_row, to_col = to_pos
        target = board[to_row][to_col]
        if target is not None and target.color == self.color:
            return False

        return True
    
    def bishop_behavior(self, board: list[list[Piece]], from_pos: tuple, to_pos: tuple) -> bool:
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
            
        return True
    
    def rook_behavior(self, board: list[list[Piece]], from_pos: tuple, to_pos: tuple) -> bool:
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        if not (from_row == to_row or from_col == to_col):
            return False

        if from_row == to_row and from_col == to_col:
            return False

        row_step = 0 if from_row == to_row else (1 if to_row > from_row else -1)
        col_step = 0 if from_col == to_col else (1 if to_col > from_col else -1)

        cur_row, cur_col = from_row + row_step, from_col + col_step
        while (cur_row, cur_col) != (to_row, to_col):
            if board[cur_row][cur_col] is not None:
                return False
            cur_row += row_step
            cur_col += col_step
            
        return True