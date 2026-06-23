import arcade
from src.ui.game_visual import GameVisual
from src.ui.game_ui import GameUI
from src.core.board import Board
from src.pieces.piece import Piece
from ..constants import HIGHLIGHT_SELECTED, BOARD_OFFSET_X, BOARD_OFFSET_Y


class GameView(arcade.View):
    def __init__(self):
        super().__init__(background_color=arcade.color.GRAY)
        
        arcade.load_font("assets/font/ARCADECLASSIC.ttf")

        self.selected = None
        self.turn = True
        self.is_pause = False

        self.board = Board()
        self.setup_board()

        self.visual = GameVisual(self.board.grid)
        self.ui = GameUI()
        self.ui.set_up_ui(self.unpause, self.restart)

    def setup_board(self):
        for row in range(8):
            for col in range(8):
                piece = self.board.get(row, col)
                if piece is not None:
                    piece.set_button_callback(lambda r=row, c=col: self.on_piece_clicked(r, c))

    def on_piece_clicked(self, row: int, col: int):
        if self.is_pause:
            return
        
        if self.selected:
            self.move_piece(self.selected, (row, col))
            self.stop_moving()
            return

        piece = self.board.get(row, col)
        if piece.color == "w" and not self.turn:
            return
        if piece.color == "b" and self.turn:
            return

        self.selected = (row, col)
        self._update_highlights()

    def move_piece(self, from_pos: tuple, to_pos: tuple):
        if not self.board.is_valid_move(from_pos, to_pos):
            return

        captured = self.board.move(from_pos, to_pos)

        if self.board.is_king_threatened(self.turn):
            self.board.undo()
            return

        if captured is not None:
            self.visual.remove_piece(captured)

        to_row, to_col = to_pos
        piece = self.board.get(to_row, to_col)
        piece.set_position(to_row, to_col)
        piece.set_button_callback(lambda r=to_row, c=to_col: self.on_piece_clicked(r, c))
        piece.pieced_moved()

        if self.board.is_checkmate(not self.turn):
            print(f"WIN {"white" if self.turn else "black"}")
        else:
            self.switch_turn()
        
    def switch_turn(self):
        self.turn = not self.turn
        self.ui.set_turn(self.turn)

    def stop_moving(self):
        self.visual.clear_highlights()
        self.selected = None

    def _update_highlights(self):
        row, col = self.selected
        highlights = [(row, col, HIGHLIGHT_SELECTED)]
        highlights.extend(self.board.get(row, col).move_hightlight(self.board.grid, self.selected))
        
        self.visual.set_highlights(highlights)
        
    def restart(self):
        self.turn = True
        self.ui.set_turn(self.turn)
        
        self.unpause()
        self.board.setup_board()
        
        self.setup_board()
        self.visual.set_board(self.board.grid)
        
    def unpause(self):
        self.is_pause = False
        self.ui.unpause()

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.TAB:
            self.is_pause = not self.is_pause
            
            if self.is_pause:
                self.ui.pause()
            else:
                self.ui.unpause()
            
        return super().on_key_press(symbol, modifiers)

    def on_mouse_press(self, x, y, button, modifiers):
        if self.is_pause:
            return

        if self.selected is not None:
            col = round((x - BOARD_OFFSET_X - 18) / 60)
            row = round((600 - BOARD_OFFSET_Y + 24 - y) / 60)

            if self.board.is_within_bounds(row, col):
                if self.board.get(row, col) is None:
                    self.move_piece(self.selected, (row, col))
                    self.stop_moving()

    def on_draw(self):
        self.clear()
        self.visual.draw()
        self.ui.draw()