import arcade
from src.ui.game_visual import GameVisual
from src.ui.game_ui import GameUI
from src.core.board import Board
from src.core.bot.bot import Bot
from ..constants import HIGHLIGHT_SELECTED, BOARD_OFFSET_X, BOARD_OFFSET_Y
from ..core.bot.evaluator import evaluate
from ..color_enum import Color

class GameView(arcade.View):
    def __init__(self, is_bot:bool = True):
        super().__init__(background_color=arcade.color.GRAY)

        self.is_bot = is_bot

        self.selected = None
        self.turn = True
        self.is_pause = False
        self.is_win = False

        self.board = Board()
        self.setup_board()
        
        self.bot = Bot(self.board)

        self.visual = GameVisual(self.board.grid)
        self.ui = GameUI()
        self.ui.set_up_ui_buttons(self.unpause, self.restart, self.main_menu)

    def setup_board(self):
        for row in range(8):
            for col in range(8):
                piece = self.board.get(row, col)
                if piece is not None:
                    piece.set_button_callback(lambda r=row, c=col: self.on_piece_clicked(r, c))

    def on_piece_clicked(self, row: int, col: int):
        if self.is_pause or self.is_win:
            return
        
        if self.selected:
            self.move_piece(self.selected, (row, col))
            self.stop_moving()
            return

        piece = self.board.get(row, col)
        if piece.color == Color.WHITE and not self.turn:
            return
        if piece.color == Color.BLACK and self.turn:
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
        
        if self.board.is_promotion():
            self.ui.show_promotion(self._on_promotion)
            return

        self.finish_turn()
    
    def _on_promotion(self, piece_type: str):
        last = self.board.last_action()
        to_row, to_col = last.to_pos

        old_piece = self.board.get(to_row, to_col)
        self.visual.remove_piece(old_piece)

        self.board.promote(piece_type)

        new_piece = self.board.get(to_row, to_col)
        self.visual.add_piece(new_piece, to_row, to_col)
        new_piece.set_button_callback(
            lambda r=to_row, c=to_col: self.on_piece_clicked(r, c)
        )

        self.finish_turn()    
    
    def finish_turn(self):
        score = evaluate(self.board)
        self.ui.update_eval(score)
        
        if self.board.is_checkmate(not self.turn):
            self._win()
            return

        self.turn = not self.turn
        self.ui.set_turn(self.turn)

        if not self.turn and self.is_bot:
            from_pos, to_pos = self.bot.get_move()
            self.move_piece(from_pos, to_pos)
        
    def _win(self):
        self.is_win = True
        self.stop_moving()
        self.ui.win(self.turn)

    def stop_moving(self):
        self.visual.clear_highlights()
        self.selected = None

    def _update_highlights(self):
        row, col = self.selected
        highlights = [(row, col, HIGHLIGHT_SELECTED)]
        
        last_action = self.board.last_action()
        
        highlights.extend(self.board.get(row, col).move_hightlight(self.board.grid, self.selected, last_action))
        
        self.visual.set_highlights(highlights)
        
    def restart(self):
        self.turn = True
        self.ui.set_turn(self.turn)
        self.ui.remove_win()
        self.is_win = False

        self.unpause()
        self.board.setup_board()

        self.setup_board()
        self.visual.set_board(self.board.grid)
    
    def main_menu(self):
        from src.view.main_menu_view import MainMenuView

        self.window.show_view(MainMenuView())
    
    def unpause(self):
        self.is_pause = False
        self.ui.unpause()

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.TAB and not self.is_win:
            self.is_pause = not self.is_pause

            if self.is_pause:
                self.ui.pause()
            else:
                self.ui.unpause()

        return super().on_key_press(symbol, modifiers)

    def on_mouse_press(self, x, y, button, modifiers):
        if self.is_pause or self.is_win:
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