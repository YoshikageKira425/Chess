import arcade
from .game_visual import GameVisual
from .game_ui import GameUI
from .pieces.piece import Piece


class GameView(arcade.View):
    def __init__(self):
        super().__init__(background_color=arcade.color.GRAY)
        
        self.selected = None
        
        self.turn = True

        self.board = [
            [Piece("bR"), Piece("bN"), Piece("bB"), Piece("bQ"), Piece("bK"), Piece("bB"), Piece("bN"), Piece("bR")],
            [Piece("bP"), Piece("bP"), Piece("bP"), Piece("bP"),Piece("bP"), Piece("bP"), Piece("bP"), Piece("bP")],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [Piece("wP"), Piece("wP"), Piece("wP"), Piece("wP"), Piece("wP"), Piece("wP"), Piece("wP"), Piece("wP")],
            [Piece("wR"), Piece("wN"), Piece("wB"), Piece("wQ"), Piece("wK"), Piece("wB"), Piece("wN"), Piece("wR")],
        ]
        self.setup_board(self.board)
        
        self.visual = GameVisual(self.board)
        self.ui = GameUI()

    def setup_board(self, board: list[list[Piece]]):
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece is not None:
                    piece.set_button_callback(lambda row=row, col=col: self.on_piece_clicked(row, col))
                    
    def on_piece_clicked(self, row: int, col: int):
        if self.selected is None:
            self.selected = (row, col)
        else:
            self.move_piece(self.selected, (row, col))

    def move_piece(self, fromPos: tuple, toPos: tuple):
        from_row, from_col = fromPos
        to_row, to_col = toPos
        
        if from_row == to_row and from_col == to_col:
            self.selected = None
            return

        piece = self.board[from_row][from_col]
        
        if piece.color == "w" and not self.turn:
            self.selected = None
            return
        
        if piece.color == "b" and self.turn:
            self.selected = None
            return
        
        captured = self.board[to_row][to_col]
        if captured is not None:
            self.visual.remove_piece(captured)

        self.board[to_row][to_col] = piece
        self.board[from_row][from_col] = None

        piece.set_position(to_row, to_col)

        piece.set_button_callback(lambda r=to_row, c=to_col: self.on_piece_clicked(r, c))

        self.selected = None
        
        self.turn = not self.turn
        self.ui.set_turn(self.turn)

    def on_mouse_press(self, x, y, button, modifiers):
        if self.selected is not None:
            col = round((x - 175 - 18) / 60)
            row = round((600 - 110 + 24 - y) / 60)

            if 0 <= row <= 7 and 0 <= col <= 7:
                to_piece = self.board[row][col]
                if to_piece is None:
                    self.move_piece(self.selected, (row, col))

    def on_draw(self):
        self.clear()
        
        self.visual.draw()
        self.ui.draw()
