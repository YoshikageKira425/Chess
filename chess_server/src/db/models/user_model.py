from sqlalchemy.orm import Mapped, mapped_column
from ..database import Base

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    elo: Mapped[int] = mapped_column(default=1000)