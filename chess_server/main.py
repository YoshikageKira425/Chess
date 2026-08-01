from fastapi import FastAPI
from src.routes import auth, games

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(games.router, prefix="/game", tags=["game"])