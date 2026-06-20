import arcade
from src.ui.game_visual import GameVisual
from src.ui.game_ui import GameUI
from src.pieces.piece import Piece
from src.pieces.pawn import Pawn
from src.pieces.knight import Knight
from src.pieces.rook import Rook
from src.pieces.bishop import Bishop
from src.pieces.queen import Queen
from ..constants import HIGHLIGHT_SELECTED, BOARD_OFFSET_X, BOARD_OFFSET_Y


class GameView(arcade.View):
    def __init__(self):
        super().__init__(background_color=arcade.color.GRAY)
        
        self.selected = None
        
        self.turn = True

        self.board = [
            [Rook("bR"), Knight("bN"), Bishop("bB"), Queen("bQ"), Piece("bK"), Bishop("bB"), Knight("bN"), Rook("bR")],
            [Pawn("bP"), Pawn("bP"), Pawn("bP"), Pawn("bP"),Pawn("bP"), Pawn("bP"), Pawn("bP"), Pawn("bP")],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [Pawn("wP"), Pawn("wP"), None, None, None, Pawn("wP"), Pawn("wP"), Pawn("wP")],
            [Rook("wR"), Knight("wN"), Bishop("wB"), Queen("wQ"), Piece("wK"), Bishop("wB"), Knight("wN"), Rook("wR")],
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
        if self.selected:
            self.move_piece(self.selected, (row, col))
            self.stop_moving()
            return
        
        piece = self.board[row][col]
        if piece.color == "w" and not self.turn:
            return
        
        if piece.color == "b" and self.turn:
            return
        
        self.selected = (row, col)
        self._update_highlights()
            
    def move_piece(self, from_pos: tuple, to_pos: tuple):
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        piece = self.board[from_row][from_col]
        
        if not piece:
            return
        
        if not piece.valid_move(self.board, from_pos, to_pos):
            return
        
        captured = self.board[to_row][to_col]
        if captured is not None:
            self.visual.remove_piece(captured)

        self.board[to_row][to_col] = piece
        self.board[from_row][from_col] = None

        piece.set_position(to_row, to_col)

        piece.set_button_callback(lambda r=to_row, c=to_col: self.on_piece_clicked(r, c))
        
        piece.pieced_moved()

        self.turn = not self.turn
        self.ui.set_turn(self.turn)
        
    def stop_moving(self):
        self.visual.clear_highlights()
        self.selected = None
        
    def _update_highlights(self):
        row, col = self.selected
        highlights = [(row, col, HIGHLIGHT_SELECTED)]  # selected square

        highlights.extend(self.board[row][col].move_hightlight(self.board, self.selected))

        self.visual.set_highlights(highlights)

    def on_mouse_press(self, x, y, button, modifiers):
        if self.selected is not None:
            col = round((x - BOARD_OFFSET_X - 18) / 60)
            row = round((600 - BOARD_OFFSET_Y + 24 - y) / 60)

            if 0 <= row <= 7 and 0 <= col <= 7:
                to_piece = self.board[row][col]
                if to_piece is None:
                    self.move_piece(self.selected, (row, col))
                    self.stop_moving()

    def on_draw(self):
        self.clear()
        
        self.visual.draw()
        self.ui.draw()
