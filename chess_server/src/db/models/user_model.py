from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class User(DeclarativeBase):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    elo: Mapped[int] = mapped_column(default=1000)