from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone
from src.db.models.game_model import Game
from src.db.models.moves_model import MoveModel
from sqlalchemy import select
from src.core.game_manager import game_manager


class GamesController:

    @staticmethod
    async def get(db: AsyncSession, game_id: int) -> Game:
        if not game_id:
            return None

        result = await db.execute(select(Game).where(Game.id == game_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def create(db: AsyncSession, white_player_id: int, black_player_id: int) -> Game:
        game = Game(
            white_player=white_player_id,
            black_player=black_player_id,
        )
        db.add(game)
        await db.commit()
        await db.refresh(game)

        game_manager.create_session(game.id, white_player_id, black_player_id)

        return game
    
    @staticmethod
    async def end(db: AsyncSession, game_id: int, winner_id: int | None = None, is_draw: bool | None = None):
        game = await GamesController.get(db, game_id)
        if not game:
            return
        
        game.winner_id = winner_id
        game.is_draw = is_draw
        game.ended_at = datetime.now(timezone.utc)
        game_manager.remove_session(game_id)
        
        await db.commit()
        await db.refresh(game)

    @staticmethod
    async def add_move(db: AsyncSession, game_id: int, from_pos: tuple, to_pos: tuple, player_id: int) -> dict:
        session = game_manager.get_session(game_id)

        if session is None:
            return {"success": False, "reason": "game not found"}

        result = session.make_move(from_pos, to_pos, player_id)

        if not result["success"]:
            return result

        from_row, from_col = from_pos
        to_row, to_col = to_pos

        move = MoveModel(game_id=game_id, from_col=from_col,
                         from_row=from_row, to_col=to_col, to_row=to_row)

        if result["status"] == "checkmate":
            GamesController.end(db, game_id, result["winner_id"])
        elif result["status"] == "stalemate":
            GamesController.end(db, game_id, None, True)

        db.add(move)
        await db.commit()

        return result