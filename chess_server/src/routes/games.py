from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.database import get_db
from src.controller.games_controller import GamesController

router = APIRouter()


@router.get("/{game_id}")
async def get_game(game_id: int, db: AsyncSession = Depends(get_db)):
    game = await GamesController.get(db, game_id)
    if game is None:
        raise HTTPException(status_code=404, detail="Game not found")
    return game


@router.post("/create")
async def create_game(white_player_id: int, black_player_id: int, db: AsyncSession = Depends(get_db)):
    game = await GamesController.create(db, white_player_id, black_player_id)
    return game
