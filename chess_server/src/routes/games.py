from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.database import get_db
from src.controller.games_controller import GamesController

router = APIRouter()

@router.post("/create")
async def create_game(white_player_id: int, black_player_id: int, db: AsyncSession = Depends(get_db)):
    game = await GamesController.create(db, white_player_id, black_player_id)
    return game

@router.post("/move-piece")
async def move_piece(game_id: int, from_pos: tuple, to_pos: tuple, player_id: int, db: AsyncSession = Depends(get_db)):
    result = await GamesController.add_move(db, game_id, from_pos, to_pos, player_id)
    return result