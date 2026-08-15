from datetime import datetime
from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from ..database import Base


class MoveModel(Base):
    __tablename__ = "moves"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )
    game_id: Mapped[int] = mapped_column(
        ForeignKey("games.id")
    )
    from_row: Mapped[int]
    from_col: Mapped[int]
    to_row: Mapped[int]
    to_col: Mapped[int]
    played_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )