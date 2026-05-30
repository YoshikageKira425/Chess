import arcade
import arcade.gui
from .pieces.piece import Piece


class GameVisual():
    def __init__(self, board: list[list[Piece]]):
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.manager._pixelated = True
        
        board_image = arcade.gui.UIImage(
            texture=arcade.load_texture("assets/sprites/board/board_with_border_01.png"),
            x=140,
            y=40,
            width=528,
            height=528
        )
        self.manager.add(board_image)
        
        self.setBoard(board)

    def setBoard(self, board: list[list[Piece]]):
        self.board = board

        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece is not None:
                    piece.setPosition(row, col) 
                    self.manager.add(piece.pieceButton)

    def draw(self):
        self.manager.draw()