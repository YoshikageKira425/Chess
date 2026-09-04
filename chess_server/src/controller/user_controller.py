from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models.user_model import User
from sqlalchemy import select


class UserController:
    @staticmethod
    async def update_elo(db: AsyncSession, player_id: int, elo: int):
        result = await db.execute(
            select(User).where(User.id == player_id)
        )

        user = result.scalar_one_or_none()

        if user is None:
            return False

        user.elo += elo

        await db.commit()
        await db.refresh(user)

        return user

    @staticmethod
    async def get_user_elo(db: AsyncSession, id: int) -> dict:
        result = await db.execute(
            select(User).where(User.id == id)
        )
        user = result.scalar_one_or_none()

        return {"elo": user.elo}
