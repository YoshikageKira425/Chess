import arcade
import arcade.gui
from ..pieces.piece import Piece
from ..constants import SQUARE_SIZE, BOARD_OFFSET_X, BOARD_OFFSET_Y


class GameVisual():
    def __init__(self, board: list[list[Piece]]):
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
        
        self.set_board(board)

    def set_board(self, board: list[list[Piece]]):
        self._pieces_holder.clear()
        self.board = board

        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece is not None:
                    piece.set_position(row, col) 
                    self._pieces_holder.add(piece.piece_button)
                    
    def add_piece(self, piece: Piece, row: int, col: int):
        piece.set_position(row, col)
        self._pieces_holder.add(piece.piece_button)            
        
    def remove_piece(self, piece: Piece):
        self._pieces_holder.remove(piece.piece_button)
        
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