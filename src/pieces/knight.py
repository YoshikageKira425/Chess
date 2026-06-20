from .piece import Piece
from ..constants import HIGHLIGHT_MOVE, HIGHLIGHT_CAPTURE

class Knight(Piece):
    def __init__(self, piece):
        super().__init__(piece)
        
    def valid_move(self, board: list[list[Piece]], from_pos: tuple, to_pos: tuple) -> bool:
        from_row, from_col = from_pos
        
        possible_moves = [(from_row + 1, from_col + 2), (from_row - 1, from_col + 2), 
                          (from_row + 2, from_col + 1), (from_row + 2, from_col - 1), 
                          (from_row - 2, from_col + 1), (from_row - 2, from_col - 1), 
                          (from_row + 1, from_col - 2), (from_row - 1, from_col - 2)]
        
        return to_pos in possible_moves
    
    def move_hightlight(self, board: list[list[Piece]], from_pos: tuple) -> list[tuple]:
        from_row, from_col = from_pos
        highlights = []
        
        possible_moves = [(from_row + 1, from_col + 2), (from_row - 1, from_col + 2), 
                          (from_row + 2, from_col + 1), (from_row + 2, from_col - 1), 
                          (from_row - 2, from_col + 1), (from_row - 2, from_col - 1), 
                          (from_row + 1, from_col - 2), (from_row - 1, from_col - 2)]
        
        for move in possible_moves:
            row, col = move
            
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