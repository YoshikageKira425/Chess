from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timezone
from src.db.models.game_model import Game
from src.db.models.user_model import User
import json


class GamesController:

    @staticmethod
    async def get(db: AsyncSession, game_id: int) -> Game | None:
        result = await db.execute(
            select(Game).where(Game.id == game_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def create(db: AsyncSession, white_player_id: int, black_player_id: int) -> Game:
        game = Game(
            white_player_id=white_player_id,
            black_player_id=black_player_id,
        )
        db.add(game)
        await db.commit()
        await db.refresh(game)
        return game

    @staticmethod
    async def add_move(db: AsyncSession, game_id: int, from_pos: tuple, to_pos: tuple) -> Game | None:
        result = await db.execute(
            select(Game).where(Game.id == game_id)
        )
        game = result.scalar_one_or_none()

        if game is None:
            return None

        moves = json.loads(game.moves)
        moves.append({"from": from_pos, "to": to_pos})
        game.moves = json.dumps(moves)

        await db.commit()
        await db.refresh(game)
        return game

    @staticmethod
    async def end(db: AsyncSession, game_id: int, winner_id: int | None, is_draw: bool = False) -> Game | None:
        result = await db.execute(
            select(Game).where(Game.id == game_id)
        )
        game = result.scalar_one_or_none()

        if game is None:
            return None

        game.winner_id = winner_id
        game.is_draw = is_draw
        game.ended_at = datetime.now(timezone.utc)

        await db.commit()
        await db.refresh(game)
        return game

    @staticmethod
    async def get_user_games(db: AsyncSession, user_id: int) -> list[Game]:
        result = await db.execute(
            select(Game).where(
                (Game.white_player_id == user_id) |
                (Game.black_player_id == user_id)
            ).order_by(Game.started_at.desc())
        )
        return result.scalars().all()
