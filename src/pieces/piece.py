from src.color_enum import Color

class Piece():
    def __init__(self, color: Color):
        self.color = color
        
        self.row = 0
        self.col = 0
        
    def valid_move(self, board: list[list[Piece]], from_pos: tuple, to_pos: tuple, last_action=None) -> bool:
        return True
    
    def move_highlight(self, board: list[list[Piece]], from_pos: tuple, last_action=None) -> list[tuple]:
        return []
        
    def set_position(self, row:int, col: int):
        self.row = row
        self.col = col

    def get_postion(self) -> tuple:
        return (self.row, self.col)
