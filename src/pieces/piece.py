import arcade
import arcade.gui
from src.color_enum import Color

textures = {
    "wp": arcade.load_texture("assets/sprites/white_pieces/pawn_white.png"),
    "wr": arcade.load_texture("assets/sprites/white_pieces/tower_white.png"),
    "wn": arcade.load_texture("assets/sprites/white_pieces/knight_white.png"),
    "wb": arcade.load_texture("assets/sprites/white_pieces/bishop_white.png"),
    "wq": arcade.load_texture("assets/sprites/white_pieces/queen_white.png"),
    "wk": arcade.load_texture("assets/sprites/white_pieces/king_white.png"),
    "bp": arcade.load_texture("assets/sprites/black_pieces/pawn_black.png"),
    "br": arcade.load_texture("assets/sprites/black_pieces/tower_black.png"),
    "bn": arcade.load_texture("assets/sprites/black_pieces/knight_black.png"),
    "bb": arcade.load_texture("assets/sprites/black_pieces/bishop_black.png"),
    "bq": arcade.load_texture("assets/sprites/black_pieces/queen_black.png"),
    "bk": arcade.load_texture("assets/sprites/black_pieces/king_black.png"),
}

class Piece():
    def __init__(self, piece: str):
        self.color = Color(piece[0])
        self.piece_button = arcade.gui.UITextureButton(
            texture=textures[piece.lower()],
            x=0,
            y=0,
            width=36,
            height=48
        )
        
        self.row = 0
        self.col = 0
        
    def set_button_callback(self, callback: callable):
        @self.piece_button.event("on_click")
        def on_click(*args, **kwargs):
            callback()
    
    def valid_move(self, board: list[list[Piece]], from_pos: tuple, to_pos: tuple, last_action=None) -> bool:
        return True
    
    def move_highlight(self, board: list[list[Piece]], from_pos: tuple, last_action=None) -> list[tuple]:
        return []
    
    def set_position_board(self, row: int, col: int):
        self.set_position(row, col)
        
        x = 175 + (col * 60) + 18
        y = 600 - (110 + (row * 60) - 24)
        self.piece_button.center_x = x
        self.piece_button.center_y = y
        
    def set_position(self, row:int, col: int):
        self.row = row
        self.col = col

    def get_postion(self) -> tuple:
        return (self.row, self.col)
