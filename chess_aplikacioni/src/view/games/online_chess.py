import arcade
from src.core.network.network_manager import NetworkManager
from ..base_chess_view import BaseChess

class OnlineGameView(BaseChess):
    def __init__(self, player_id: int):
        super().__init__()
        
        self.network = NetworkManager(player_id)
        self.network.on_match_found = self._on_match_found
        self.network.on_move_received = self._on_move_received
        self.network.on_game_over = self._game_over
        self.network.on_opponent_disconnected = self.back

    def _on_match_found(self, data: dict):
        self.my_color = data["color"]
        # initialize board, visuals etc

    def _on_move_received(self, from_pos:tuple, to_pos:tuple):
        # opponent moved — update local board and visuals
        self.board.move(tuple(from_pos), tuple(to_pos))
        self.visual.update_board(self.board.grid, self.on_piece_clicked)
        
    def _game_over(self, data: dict):
        pass

    def back(self):
        from ..menus.multiplayer_menu_view import MultiplayerMenuView
        self.window.show_view(MultiplayerMenuView())

    async def move_piece(self, from_pos, to_pos):
        if not self.board.is_valid_move(from_pos, to_pos):
            return
        
        await self.network.send_move(from_pos, to_pos)
        
        self.board.move(from_pos, to_pos)
        self.visual.update_board(self.board.grid, self.on_piece_clicked)
        
        self.finish_turn()