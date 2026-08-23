from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, DateTime, Enum
from src.enum.game_status import GameStatus
from chess_core.enum.game_type import GameType
from datetime import datetime
from ..database import Base


class Game(Base):
    __tablename__ = "games"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    white_player: Mapped[int] = mapped_column(ForeignKey("users.id"))
    black_player: Mapped[int] = mapped_column(ForeignKey("users.id"))
    status: Mapped[GameStatus] = mapped_column(
        Enum(GameStatus),
        default=GameStatus.ON_GOING
    )
    type: Mapped[GameType] = mapped_column(
        Enum(GameType),
        default=GameType.CASUAL
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )
