from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.db.models.user_model import User

class LeaderboardController:
    
    @staticmethod
    async def get_leaderboard(db: AsyncSession) -> dict:
        result = await db.execute(
            select(User).order_by(User.elo.desc()).limit(10)
        )
        users = result.scalars().all()
        return [{"username": u.username, "elo": u.elo} for u in users]