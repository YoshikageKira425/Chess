import arcade
from ..base_chess_view import BaseChess
from src.visual.pause_ui import PauseUi
from src.enum.color_enum import Color
from src.core.bot.evaluator import evaluate

class LocalChess(BaseChess):
    def __init__(self):
        super().__init__()
        
        self._is_paused = False
        self._pause_ui = PauseUi()
        
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
            self._is_paused = not self._is_paused
            self._pause_ui.pause(self._is_paused)
    
    def on_draw(self):
        super().on_draw()
        
        self._pause_ui.draw()