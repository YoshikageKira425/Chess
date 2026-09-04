from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.routes import auth, games, leaderboard
from src.db.database import init_db
from src.core.game_manager import game_manager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    app.state.game_manager = game_manager
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(games.router, prefix="/game", tags=["game"])
app.include_router(leaderboard.router, prefix="/leaderboard", tags=["leaderboard"])