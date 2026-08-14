from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone
from src.db.models.game_model import Game
import json
from src.core.game_manager import game_manager

class GamesController:

    @staticmethod
    async def create(db: AsyncSession, white_player_id: int, black_player_id: int) -> Game:
        game = Game(
            white_player_id=white_player_id,
            black_player_id=black_player_id,
        )
        db.add(game)
        await db.commit()
        await db.refresh(game)

        game_manager.create_session(game.id, white_player_id, black_player_id)

        return game

    @staticmethod
    async def add_move(db: AsyncSession, game_id: int, from_pos: tuple, to_pos: tuple, player_id: int) -> dict:
        session = game_manager.get_session(game_id)

        if session is None:
            return {"success": False, "reason": "game not found"}

        result = session.make_move(from_pos, to_pos, player_id)

        if not result["success"]:
            return result

        game = await GamesController.get(db, game_id)
        moves = json.loads(game.moves)
        moves.append({"from": from_pos, "to": to_pos})
        game.moves = json.dumps(moves)

        if result["status"] == "checkmate":
            game.winner_id = player_id
            game.ended_at = datetime.now(timezone.utc)
            game_manager.remove_session(game_id)

        elif result["status"] == "stalemate":
            game.is_draw = True
            game.ended_at = datetime.now(timezone.utc)
            game_manager.remove_session(game_id)

        await db.commit()
        await db.refresh(game)

        return result