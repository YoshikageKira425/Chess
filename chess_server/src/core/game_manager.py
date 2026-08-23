from chess_core.board import Board
from chess_core.enum.color_enum import Color
from src.enum.game_type import GameType


class GameSession:
    def __init__(self, game_id: int, white_player_id: int, black_player_id: int, type: GameType):
        self.game_id = game_id
        self.white_player_id = white_player_id
        self.black_player_id = black_player_id
        self.type = type
        
        self.board = Board()
        self.turn = Color.WHITE

    def get_current_player_id(self) -> int:
        return self.white_player_id if self.turn == Color.WHITE else self.black_player_id

    def is_casual_match(self) -> bool:
        return self.type == GameType.CASUAL

    def make_move(self, from_pos: tuple, to_pos: tuple, player_id: int) -> dict:
        if player_id != self.get_current_player_id():
            return {"success": False, "reason": "not your turn"}

        if not self.board.is_valid_move(from_pos, to_pos):
            return {"success": False, "reason": "invalid move"}

        self.board.move(from_pos, to_pos)

        if self.board.is_king_threatened(self.turn):
            self.board.undo()
            return {"success": False, "reason": "move leaves king in check"}

        next_turn = Color.BLACK if self.turn == Color.WHITE else Color.WHITE

        if self.board.is_checkmate(next_turn):
            return {"success": True, "status": "checkmate", "winner_id": player_id}

        if self.board.is_stalemate(next_turn):
            return {"success": True, "status": "stalemate"}

        self.turn = next_turn
        return {"success": True, "status": "continue"}


class GameManager:
    def __init__(self):
        self._sessions: dict[int, GameSession] = {}

    def create_session(self, game_id: int, white_player_id: int, black_player_id: int, type: GameType) -> GameSession:
        session = GameSession(game_id, white_player_id, black_player_id, type)
        self._sessions[game_id] = session
        return session

    def get_session(self, game_id: int) -> GameSession | None:
        return self._sessions.get(game_id)

    def remove_session(self, game_id: int):
        self._sessions.pop(game_id, None)

game_manager = GameManager()