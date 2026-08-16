import arcade
from src.core.network.network_manager import NetworkManager
from ..base_chess_view import BaseChess
from src.visual.online_information_ui import OnlineInformationUI
from src.visual.end_screen_ui import EndScreenUi
from src.visual.finding_match_ui import FindingMatchUI
from src.constants import BOARD_OFFSET_X, BOARD_OFFSET_Y
from src.core.evaluator import evaluate
from chess_core.enum.color_enum import Color 

class OnlineGameView(BaseChess):
    def __init__(self, player_id: int):
        super().__init__()
        
        self._showing_visuals = False
        self_my_turn = False

        self.player_id = player_id

        self.network = NetworkManager(player_id)
        self.network.on_match_found = self._on_match_found
        self.network.on_move_received = self._on_move_received
        self.network.on_game_over = self._game_over
        self.network.on_opponent_disconnected = self.back

        self.ui = OnlineInformationUI()
        self.loading_ui = FindingMatchUI()
        self.end_screen_ui = EndScreenUi()
        
        self.end_screen_ui.set_up_ui_buttons(None, self.back)

    def _on_match_found(self, data: dict):
        self._showing_visuals = True
    
        self.my_color = data["color"]
        self.ui.set_color(self.my_color)
        self._my_turn = self.my_color == Color.WHITE

    def _on_move_received(self, from_pos: tuple, to_pos: tuple):
        self.board.move(tuple(from_pos), tuple(to_pos))
        self.updated_visuals(evaluate(self.board))
        self._stop_moving()
        
        self._my_turn = True

    def _game_over(self, data: dict):
        self.is_match_finished = True
        
        status = data.get("status")
        
        if status == "checkmate":
            winner = data["winner_id"]
            color = None
            
            if winner == self.player_id:
                color = self.my_color
            else:
                color = Color.WHITE if self.my_color == Color.BLACK else Color.BLACK
                
            self.end_screen_ui.show_end_screen(color)
        else:
            self.end_screen_ui.show_end_screen()

    def back(self):
        from ..menus.multiplayer_menu_view import MultiplayerMenuView
        self.window.show_view(MultiplayerMenuView())

    def on_piece_clicked(self, row: int, col: int):
        if self.is_match_finished or not self._my_turn:
            return

        if self.selected:
            self.move_piece(self.selected, (row, col))
            self._stop_moving()
            return

        piece = self.board.get(row, col)
        if piece is None:
            return

        if piece.color != self.my_color:
            return

        self.selected = (row, col)
        self._update_highlights()

    def move_piece(self, from_pos, to_pos):
        if not self.board.is_valid_move(from_pos, to_pos):
            return

        self._my_turn = False
        self.network.send_move(from_pos, to_pos)

        self.board.move(from_pos, to_pos)
        self.visual.update_board(self.board.grid, self.on_piece_clicked)

        self.updated_visuals(evaluate(self.board))
        self._stop_moving()

    def on_update(self, delta_time: float):
        self.end_screen_ui.update(delta_time)

    def on_draw(self):
        if self._showing_visuals:
            super().on_draw()
            
            self.ui.draw()
            self.end_screen_ui.draw()
        else:
            self.clear()
            self.loading_ui.draw()
