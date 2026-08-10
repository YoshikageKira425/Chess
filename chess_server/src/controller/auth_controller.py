from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.db.models.user_model import User
import bcrypt


class AuthController:

    @staticmethod
    async def login(db: AsyncSession, username: str, password: str) -> User | None:
        result = await db.execute(
            select(User).where(User.username == username)
        )
        user = result.scalar_one_or_none()

        if user is None:
            return None

        if not bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
            return None

        return user

    @staticmethod
    async def signup(db: AsyncSession, username: str, password: str) -> User | None:
        if username is None or password is None:
            return None

        if len(password) < 8:
            return None

        result = await db.execute(
            select(User).where(User.username == username)
        )
        existing = result.scalar_one_or_none()
        if existing is not None:
            return None

        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

        new_user = User(username=username, password=password_hash)

        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)

        return new_user