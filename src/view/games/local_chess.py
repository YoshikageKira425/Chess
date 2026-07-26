import arcade
from ..base_chess_view import BaseChess
from src.visual.pause_ui import PauseUi
from src.core.bot.evaluator import evaluate

class LocalChess(BaseChess):
    def __init__(self):
        super().__init__()
        
        self._pause_ui = PauseUi()
        self._pause_ui.set_up_ui_buttons(self.pause, self.restart, self.main_menu)
        
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
    
    def pause(self):
        self._is_paused = not self._is_paused
        self._pause_ui.pause(self._is_paused)
        
    def restart(self):
        self.pause()
        self.board.setup_board()
        self.setup_game()
        self.visual.clear_highlights()
        
    def main_menu(self):
        from src.view.main_menu_view import MainMenuView

        self.window.show_view(MainMenuView())
    
    def on_draw(self):
        super().on_draw()
        
        self._pause_ui.draw()