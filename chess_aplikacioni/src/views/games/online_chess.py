import arcade
from src.core.network.network_manager import NetworkManager
from ..base.base_chess_view import BaseChess
from src.ui.online_information_ui import OnlineInformationUI
from src.ui.end_screen_ui import EndScreenUi
from src.ui.finding_match_ui import FindingMatchUI
from src.ui.pause_online_ui import PauseUi
from src.constants import BOARD_OFFSET_X, BOARD_OFFSET_Y
from src.core.ai.evaluator import evaluate
from chess_core.enum.color_enum import Color


class OnlineGameView(BaseChess):
    def __init__(self, player_id: int):
        super().__init__()

        self._showing_visuals = False
        self._my_turn = False

        self.player_id = player_id

        self.network = NetworkManager(player_id)

        self.ui = OnlineInformationUI()
        self.loading_ui = FindingMatchUI()
        self.pause_ui = PauseUi()
        self.end_screen_ui = EndScreenUi()

        self._is_paused = False

        self.pause_ui.set_up_ui_buttons(self.pause, self.disconnect)
        self.end_screen_ui.set_up_ui_buttons(self.replay, self.back)

    def on_update(self, delta_time: float):
        self.end_screen_ui.update(delta_time)
        self.pause_ui.update(delta_time)
        
        self._process_network_events()

    def on_key_press(self, symbol, modifiers):
        if symbol in [arcade.key.TAB, arcade.key.ESCAPE, arcade.key.P] and not self.is_match_finished:
            self.pause()

    def on_draw(self):
        if self._showing_visuals:
            super().on_draw()

            self.ui.draw()
            self.pause_ui.draw()
            self.end_screen_ui.draw()
        else:
            self.clear()
            self.loading_ui.draw()

    def _process_network_events(self):
        while not self.network.events.empty():
            data = self.network.events.get()
            
            match data.get("type"):
                case "match_found":
                    self._handle_match_found(Color(data["color"]))
                case "move":
                    self._handle_opponent_move(data["from"], data["to"])
                case "game_over":
                    self._handle_game_over(data["status"], data.get("winner_id"))
                case "opponent_disconnected":
                    self.back()

    def _handle_match_found(self, color: Color):
        self._showing_visuals = True

        self.my_color = color
        self.ui.set_color(self.my_color)
        self._my_turn = self.my_color == Color.WHITE

    def _handle_opponent_move(self, from_pos: tuple, to_pos: tuple):
        self.board.move(tuple(from_pos), tuple(to_pos))
        self.updated_visuals(evaluate(self.board))
        self._stop_moving()

        self._my_turn = True
        self.information.set_turn(self.my_color)

    def _handle_game_over(self, status: str, winner_id: int):
        self.is_match_finished = True

        if status == "checkmate":
            color = None

            if winner_id == self.player_id:
                color = self.my_color
            else:
                color = self.my_color.inverted()

            self.end_screen_ui.show_end_screen(color)
        elif status == "stalemate":
            self.end_screen_ui.show_end_screen()
        else:
            self.end_screen_ui.show_end_screen(custom_label="Resigned")

    def disconnect(self):
        self.network.resign()
        
        self.back()

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
        self.information.set_turn(self.my_color.inverted())

    def pause(self):
        self._is_paused = not self._is_paused
        self.pause_ui.pause(self._is_paused)
    
    def replay(self):
        self.window.show_view(OnlineGameView(self.player_id))
