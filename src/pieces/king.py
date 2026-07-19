from .piece import Piece
from ..constants import HIGHLIGHT_MOVE, HIGHLIGHT_CAPTURE

class King(Piece):
    def __init__(self, piece):
        super().__init__(piece)
        
    def valid_move(self, board: list[list[Piece]], from_pos: tuple, to_pos: tuple, last_action=None) -> bool:
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
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
            
            piece = board[row][col]
            
            if row == to_row and col == to_col:
                if piece is None:
                    return True
                elif piece.color != self.color:
                    return True
                
                return False
        
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
            
            piece = board[row][col]
            
            if piece is None:
                highlights.append((row, col, HIGHLIGHT_MOVE))
            elif piece.color != self.color:
                highlights.append((row, col, HIGHLIGHT_CAPTURE))
        
        return highlights