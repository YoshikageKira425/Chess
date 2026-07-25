import arcade
from src.ui.game_visual import GameVisual
from src.ui.game_ui import GameUI
from src.core.board import Board
from ..constants import HIGHLIGHT_SELECTED, HIGHLIGHT_CAPTURE, BOARD_OFFSET_X, BOARD_OFFSET_Y
from ..core.bot.evaluator import evaluate
from ..enum.color_enum import Color

class GameView(arcade.View):
    def __init__(self):
        super().__init__(background_color=arcade.color.GRAY)

        self.board = Board()

        self.visual = GameVisual()
        self.ui = GameUI()
        
        self.ui.set_up_ui_buttons(self.unpause, self.restart, self.main_menu)
        
        self.setup_game()    

    def setup_game(self):
        self.selected = None
        self.turn = Color.WHITE
        self.is_match_finished = False
        self.score = 0
        
        self.visual.update_board(self.board.grid, self.on_piece_clicked)

    def on_piece_clicked(self, row: int, col: int):
        if self.is_match_finished:
            return
        
        if self.selected:
            self.move_piece(self.selected, (row, col))
            self.stop_moving()
            return

        piece = self.board.get(row, col)
        if piece is None:
            return
        
        if piece.color != self.turn:
            return

        self.selected = (row, col)
        self._update_highlights()

    def move_piece(self, from_pos: tuple, to_pos: tuple):
        if not self.board.is_valid_move(from_pos, to_pos):
            return

        self.board.move(from_pos, to_pos)

        if self.board.is_king_threatened(self.turn):
            self.board.undo()
            return
        
        if self.board.is_promotion():
            self.promotion()
            return

        self.finish_turn()
    
    def promotion(self):
        pass   
    
    def finish_turn(self):
        self.visual.update_board(self.board.grid, self.on_piece_clicked)
        self.score = evaluate(self.board)
        
        if self.board.is_stalemate(self.turn):
            self._stalemate()
            return
        
        if self.board.is_checkmate(self.turn):
            self._win()
            return

        self.turn = Color.WHITE if self.turn == Color.BLACK else Color.BLACK
        
    def _win(self):
        self.is_match_finished = True
        self.stop_moving()
        
    def _stalemate(self):
        self.is_match_finished = True
        self.stop_moving()

    def stop_moving(self):
        self.visual.clear_highlights()
        self.selected = None

    def _update_highlights(self):
        row, col = self.selected
        highlights = [(row, col, HIGHLIGHT_SELECTED)]
        
        last_action = self.board.last_action()
        
        highlights.extend(self.board.get(row, col).move_highlight(self.board.grid, self.selected, last_action))
        
        if self.board.is_king_threatened(self.turn):
            king = self.board.white_king if self.turn else self.board.black_king
             
            highlights.append((king.row, king.col, HIGHLIGHT_CAPTURE))
        
        self.visual.set_highlights(highlights)
        
    def on_mouse_press(self, x, y, button, modifiers):
        if self.is_pause or self.is_match_finished:
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