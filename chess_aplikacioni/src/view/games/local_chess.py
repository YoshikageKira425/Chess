import arcade
from ..base_chess_view import BaseChess
from src.visual.pause_ui import PauseUi
from src.visual.end_screen_ui import EndScreenUi
from src.visual.promotion_ui import PromotionUi
from src.core.evaluator import evaluate
from chess_core.enum.color_enum import Color
from chess_core.enum.pieces_enum import Pieces

class LocalChess(BaseChess):
    def __init__(self):
        super().__init__()
        
        self._pause_ui = PauseUi()
        self._promotion_ui = PromotionUi()
        self._end_screen_ui = EndScreenUi()
        
        self._pause_ui.set_up_ui_buttons(self.pause, self.restart, self.main_menu)
        self._end_screen_ui.set_up_ui_buttons(self.restart, self.main_menu)
        
    def setup_game(self):
        self._is_paused = False
        
        return super().setup_game()
        
    def on_piece_clicked(self, row, col):
        if self._is_paused:
            return
        
        return super().on_piece_clicked(row, col)
    
    def on_mouse_press(self, x, y, button, modifiers):
        if self._is_paused:
            return
        
        return super().on_mouse_press(x, y, button, modifiers)
    
    def on_key_press(self, symbol, modifiers):
        if symbol in [arcade.key.TAB, arcade.key.ESCAPE, arcade.key.P] and not self.is_match_finished:
            self.pause()
            
        if symbol == arcade.key.SPACE and not self.is_match_finished and self.board.actions:
            self.undo()
    
    def promotion(self):
        self._promotion_ui.show_promotion(self._promotion_pawn)
        
    def _promotion_pawn(self, piece_type: Pieces):
        self.board.promote(piece_type)
        self.finish_turn()
    
    def win(self):
        oppsite = Color.BLACK if self.turn == Color.WHITE else Color.WHITE
        
        self._end_screen_ui.show_end_screen(oppsite)
        return super().win()
    
    def stalemate(self):
        self._end_screen_ui.show_end_screen()
        return super().stalemate()
    
    def undo(self):
        self.board.undo()
        self.turn = Color.WHITE if self.turn == Color.BLACK else Color.BLACK
        self.updated_visuals(evaluate(self.board))
    
    def pause(self):
        self._is_paused = not self._is_paused
        self._pause_ui.pause(self._is_paused)
        
    def restart(self):
        self.pause()
        self._end_screen_ui.hide_end_screen()
        
        self.board.setup_board()
        self.setup_game()
        self.visual.clear_highlights()
        
    def main_menu(self):
        from ..menus.main_menu_view import MainMenuView

        self.window.show_view(MainMenuView())
    
    def on_update(self, delta_time: float):
        self._pause_ui.update(delta_time)
        self._end_screen_ui.update(delta_time)

    def on_draw(self):
        super().on_draw()

        self._pause_ui.draw()
        self._promotion_ui.draw()
        self._end_screen_ui.draw()