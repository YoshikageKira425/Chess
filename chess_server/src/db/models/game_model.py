from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, DateTime
from datetime import datetime
from src.enum.game_status import GameStatus
from ..database import Base

class Game(Base):
    __tablename__ = "games"
    
    id: Mapped[str] = mapped_column(primary_key=True, autoincrement=True)
    white_player: Mapped[int] = mapped_column(ForeignKey("users.id"))
    black_player: Mapped[int] = mapped_column(ForeignKey("users.id"))
    status: Mapped[GameStatus] = mapped_column(default=GameStatus.ON_GOING)
    created_at: Mapped[datetime] = mapped_column(default=DateTime())