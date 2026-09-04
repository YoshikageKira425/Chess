from .piece import Piece
from .._constants import HIGHLIGHT_MOVE, HIGHLIGHT_CAPTURE

class King(Piece):
    def __init__(self, piece):
        super().__init__(piece)
        
        self.has_moved = False
        
    def valid_move(self, board: list[list[Piece]], from_pos: tuple, to_pos: tuple, last_action=None) -> bool:
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        if abs(to_row - from_row) <= 1 and abs(to_col - from_col) <= 1:
            if from_pos == to_pos:
                return False
            target = board[to_row][to_col]
            
            return target is None or target.color != self.color

        if not self.has_moved and from_row == to_row and abs(to_col - from_col) == 2:
            return self._can_castle(board, from_pos, to_col)
        
        return False
    
    def move_highlight(self, board: list[list[Piece]], from_pos: tuple, last_action=None) -> list[tuple]:
        from_row, from_col = from_pos
        highlights = []
        
        move_directions = [(1, 0), (1, 1), (1, -1), 
                          (0, 1), (0, -1), 
                          (-1, 0), (-1, 1), (-1, -1)]
        
        for move in move_directions:
            row, col = move
            row, col = row + from_row, col + from_col
            
            if row >= 8 or col >= 8:
                continue
            
            if row < 0 or col < 0:
                continue
            
            if self._is_cell_being_attacked(board, (row, col)):
                continue
            
            piece = board[row][col]
            
            if piece is None:
                highlights.append((row, col, HIGHLIGHT_MOVE))
            elif piece.color != self.color:
                highlights.append((row, col, HIGHLIGHT_CAPTURE))
        
        if not self.has_moved:
            from_row, from_col = from_pos
            for to_col in (6, 2):  
                if self._can_castle(board, from_pos, to_col):
                    highlights.append((from_row, to_col, HIGHLIGHT_MOVE))
        
        return highlights
    
    def _can_castle(self, board, from_pos, to_col) -> bool:
        from_row, from_col = from_pos
        rook_col = 7 if to_col == 6 else 0

        rook = board[from_row][rook_col]
        if rook is None or not hasattr(rook, 'has_moved') or rook.has_moved:
            return False

        step = 1 if rook_col > from_col else -1
        for col in range(from_col + step, rook_col, step):
            if board[from_row][col] is not None:
                return False

        pass_col = from_col + step
        for col in (from_col, pass_col, to_col):
            if self._is_cell_being_attacked(board, (from_row, col)):
                return False

        return True
    
    def _is_cell_being_attacked(self, board: list[list[Piece]], to_pos: tuple) -> bool:
        for r in range(8):
            for c in range(8):
                piece = board[r][c]
                    
                if piece is None:
                    continue
                    
                if self.color != piece.color and piece.valid_move(board, piece.get_postion(), to_pos):
                    return True
                
        return False