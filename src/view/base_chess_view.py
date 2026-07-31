import arcade
from src.visual.chess_visual import ChessVisual
from src.visual.chess_information_ui import ChessInformationUi
from src.core.board import Board
from ..constants import HIGHLIGHT_SELECTED, HIGHLIGHT_CAPTURE, BOARD_OFFSET_X, BOARD_OFFSET_Y
from ..core.evaluator import evaluate
from ..enum.color_enum import Color

class BaseChess(arcade.View):
    def __init__(self):
        super().__init__(background_color=arcade.color.HUNTER_GREEN)

        self.board = Board()

        self.visual = ChessVisual()
        self.information = ChessInformationUi()
        
        self.setup_game()    

    def setup_game(self):
        self.selected = None
        self.turn = Color.WHITE
        self.is_match_finished = False
        
        self.updated_visuals(0)

    def on_piece_clicked(self, row: int, col: int):
        if self.is_match_finished:
            return
        
        if self.selected:
            self._move_piece(self.selected, (row, col))
            self._stop_moving()
            return

        piece = self.board.get(row, col)
        if piece is None:
            return
        
        if piece.color != self.turn:
            return

        self.selected = (row, col)
        self._update_highlights()

    def _move_piece(self, from_pos: tuple, to_pos: tuple):
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
        self.turn = Color.WHITE if self.turn == Color.BLACK else Color.BLACK
        self.updated_visuals(evaluate(self.board))
        
        if self.board.is_stalemate(self.turn):
            self.stalemate()
            return
        
        if self.board.is_checkmate(self.turn):
            self.win()
            return
        
    def win(self):
        self.is_match_finished = True
        self._stop_moving()
        print("WIN")
        
    def stalemate(self):
        self.is_match_finished = True
        self._stop_moving()
        print("STALEMATE")
        
    def updated_visuals(self, evaluate_value: float):
        self.information.set_turn(self.turn)
        self.information.set_evaluator(evaluate_value)
        self.visual.update_board(self.board.grid, self.on_piece_clicked)

    def _stop_moving(self):
        self.visual.clear_highlights()
        self.selected = None

    def _update_highlights(self):
        row, col = self.selected
        highlights = [(row, col, HIGHLIGHT_SELECTED)]
        
        last_action = self.board.last_action()
        
        highlights.extend(self.board.get(row, col).move_highlight(self.board.grid, self.selected, last_action))
        
        if self.board.is_king_threatened(self.turn):
            king = self.board.white_king if self.turn == Color.WHITE else self.board.black_king
             
            highlights.append((king.row, king.col, HIGHLIGHT_CAPTURE))
        
        self.visual.set_highlights(highlights)
        
    def on_mouse_press(self, x, y, button, modifiers):
        if self.is_match_finished:
            return

        if self.selected is not None:
            col = round((x - BOARD_OFFSET_X - 18) / 60)
            row = round((600 - BOARD_OFFSET_Y + 24 - y) / 60)

            if self.board.is_within_bounds(row, col):
                if self.board.get(row, col) is None:
                    self._move_piece(self.selected, (row, col))
                    self._stop_moving()

    def on_draw(self):
        self.clear()
        
        self.visual.draw()
        self.information.draw()