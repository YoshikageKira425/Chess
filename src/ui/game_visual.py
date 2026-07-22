import arcade
import arcade.gui
from src.pieces.pawn import Pawn
from src.pieces.knight import Knight
from src.pieces.rook import Rook
from src.pieces.bishop import Bishop
from src.pieces.queen import Queen
from src.pieces.king import King
from ..pieces.piece import Piece
from ..constants import SQUARE_SIZE, BOARD_OFFSET_X, BOARD_OFFSET_Y

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

class GameVisual():
    def __init__(self):
        self._manager = arcade.gui.UIManager()
        self._manager.enable()
        self._manager._pixelated = True
        self._highlights = []
        
        board_image = arcade.gui.UIImage(
            texture=arcade.load_texture("assets/sprites/board/board_with_border_01.png"),
            x=140,
            y=40,
            width=528,
            height=528
        )
        self._manager.add(board_image)
        self._pieces_holder = arcade.gui.UIWidget()
        self._manager.add(self._pieces_holder)

    def update_board(self, board: list[list[Piece]], click_callback):
        self._pieces_holder.clear()

        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece is not None:
                    self._add_piece(piece, row, col, click_callback)
                    
    def _add_piece(self, piece: Piece, row: int, col: int, click_callback):
        types = {Pawn: "p", Knight: "n", Rook:"r", Bishop: "b", Queen: "q", King: "k"}
        
        texture = textures[f"{piece.color}{types.get(type(piece), "p")}"]
        x = 175 + (col * 60)
        y = 600 - (110 + (row * 60))
        
        piece_button = arcade.gui.UITextureButton(
            texture=texture,
            x=x,
            y=y,
            width=36,
            height=48
        )
        
        @piece_button.event("on_click")
        def on_click(*args, r=row, c=col):
            click_callback(r, c)
        
        self._pieces_holder.add(piece_button)            
        
    def set_highlights(self, squares: list[tuple]):
        """Pass in a list of (row, col) tuples to highlight."""
        self._highlights = squares

    def clear_highlights(self):
        self._highlights = []

    def _square_to_screen(self, row, col):
        x = BOARD_OFFSET_X + col * SQUARE_SIZE
        y = BOARD_OFFSET_Y + (7 - row) * SQUARE_SIZE
        return x, y

    def _draw_highlights(self):
        for row, col, color in self._highlights:
            x, y = self._square_to_screen(row, col)
            arcade.draw_rect_filled(
                arcade.XYWH(x, y, SQUARE_SIZE, SQUARE_SIZE),
                color
            )

    def draw(self):
        self._manager.draw()
        self._draw_highlights()