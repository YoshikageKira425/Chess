import arcade
import arcade.gui

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
        self.pieceButton = arcade.gui.UITextureButton(
            texture=textures[piece.lower()],
            x=0,
            y=0,
            width=36,
            height=48
        )
        
    def setPosition(self, row: int, col: int):
        x = 175 + (col * 60) + 18
        y = 600 - (110 + (row * 60) - 24)
        
        self.pieceButton.center_x = x
        self.pieceButton.center_y = y
