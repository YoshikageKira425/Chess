from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import ForeignKey, DateTime
from datetime import datetime

class GameMove(DeclarativeBase):
    __tablename__ = "game_moves"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    game_id: Mapped[int] = mapped_column(ForeignKey("games.id"))
    from_pos: Mapped[tuple[int]]
    to_pos: Mapped[tuple[int]]
    played_at: Mapped[datetime] = mapped_column(default=DateTime())
    