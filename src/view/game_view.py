import arcade
import random
from src.ui.game_visual import GameVisual
from src.ui.game_ui import GameUI
from src.core.board import Board
from src.core.bot.bot import Bot
from ..constants import HIGHLIGHT_SELECTED, HIGHLIGHT_CAPTURE, BOARD_OFFSET_X, BOARD_OFFSET_Y
from ..core.bot.evaluator import evaluate
from ..color_enum import Color
from ..action import Action

class GameView(arcade.View):
    def __init__(self, is_bot:bool = True, difficulty: str = "easy"):
        super().__init__(background_color=arcade.color.GRAY)

        self.selected = None
        self.turn = True
        self.is_pause = False
        self.is_win = False

        self.board = Board()
        self.setup_board()

        self.visual = GameVisual(self.board.grid)
        self.ui = GameUI()
        self.ui.set_up_ui_buttons(self.unpause, self.restart, self.main_menu)
        
        self.is_bot = is_bot
        self.your_color = Color.BLACK if random.random() > 0.5 else Color.WHITE
        bot_color = Color.WHITE if self.your_color == Color.BLACK else Color.BLACK
        self.bot = Bot(self.board, bot_color, difficulty)
            
        if self.your_color == Color.BLACK and is_bot:
            self.bot_move()

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

        if self.is_bot and self.bot.bot_color == (Color.WHITE if self.turn else Color.BLACK):
            self.bot_move()
        
    def _win(self):
        self.is_win = True
        self.stop_moving()
        self.ui.win(self.turn)

    def bot_move(self):
        from_pos, to_pos = self.bot.get_move()
        
        if from_pos and to_pos:
            self.move_piece(from_pos, to_pos)

    def stop_moving(self):
        self.visual.clear_highlights()
        self.selected = None

    def _update_highlights(self):
        row, col = self.selected
        highlights = [(row, col, HIGHLIGHT_SELECTED)]
        
        last_action = self.board.last_action()
        
        highlights.extend(self.board.get(row, col).move_hightlight(self.board.grid, self.selected, last_action))
        
        if self.board.is_king_threatened(self.turn):
            king = self.board.white_king if self.turn else self.board.black_king
             
            highlights.append((king.row, king.col, HIGHLIGHT_CAPTURE))
        
        self.visual.set_highlights(highlights)
        
    def restart(self):
        self.turn = True
        
        self.your_color = Color.BLACK if random.random() > 0.5 else Color.WHITE
        self.bot.bot_color = Color.WHITE if self.your_color == Color.BLACK else Color.BLACK
        
        self.ui.set_turn(self.turn)
        self.ui.remove_win()
        self.is_win = False

        self.unpause()
        self.board.setup_board()
        self.stop_moving()

        self.setup_board()
        self.visual.set_board(self.board.grid)
        
        if self.your_color == Color.BLACK and self.is_bot:
            self.bot_move()
    
    def main_menu(self):
        from src.view.main_menu_view import MainMenuView

        self.window.show_view(MainMenuView())
    
    def unpause(self):
        self.is_pause = False
        self.ui.unpause()

    def on_key_press(self, symbol, modifiers):
        if symbol in [arcade.key.TAB, arcade.key.ESCAPE, arcade.key.P] and not self.is_win:
            self.is_pause = not self.is_pause

            if self.is_pause:
                self.ui.pause()
            else:
                self.ui.unpause()
                
        if symbol == arcade.key.SPACE and not self.is_win and self.board.actions:
            action = self.board.undo()
            if action:
                self._undo_visual(action)
                
            if self.is_bot:
                action = self.board.undo()
                if action:
                    self._undo_visual(action)

            score = evaluate(self.board)
            self.ui.update_eval(score)
            self.turn = not self.turn  
            self.ui.set_turn(self.turn)
            self.stop_moving()

        return super().on_key_press(symbol, modifiers)
    
    def _undo_visual(self, action: Action):
        piece = action.piece
        from_row, from_col = action.from_pos
        piece.set_position(from_row, from_col)
        piece.set_button_callback(lambda r=from_row, c=from_col: self.on_piece_clicked(r, c))

        if action.captured is not None:
            captured = action.captured

            self.visual.add_piece(captured, captured.row, captured.col)

            captured.set_button_callback(
                lambda r=captured.row, c=captured.col: self.on_piece_clicked(r, c)
            )
            
        if action.original_piece is not None:
            original_piece = action.original_piece

            self.visual.add_piece(original_piece, original_piece.row, original_piece.col)
            self.visual.remove_piece(action.piece)

            original_piece.set_button_callback(
                lambda r=original_piece.row, c=original_piece.col: self.on_piece_clicked(r, c)
            )

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