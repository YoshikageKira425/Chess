import arcade
import arcade.gui
from ..pieces.piece import Piece


class GameVisual():
    def __init__(self, board: list[list[Piece]]):
        self._manager = arcade.gui.UIManager()
        self._manager.enable()
        self._manager._pixelated = True
        
        board_image = arcade.gui.UIImage(
            texture=arcade.load_texture("assets/sprites/board/board_with_border_01.png"),
            x=140,
            y=40,
            width=528,
            height=528
        )
        self._manager.add(board_image)
        
        self.set_board(board)

    def set_board(self, board: list[list[Piece]]):
        self.board = board

        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece is not None:
                    piece.set_position(row, col) 
                    self._manager.add(piece.piece_button)
                    
    def remove_piece(self, piece: Piece):
        self._manager.remove(piece.piece_button)

    def draw(self):
        self._manager.draw()