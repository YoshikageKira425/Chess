from fastapi import APIRouter,  Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.database import get_db
from src.controller.leaderboard_controller import LeaderboardController
from src.controller.user_controller import UserController

router = APIRouter()

@router.get("/")
async def get_leaderboard(db: AsyncSession = Depends(get_db)):
    return await LeaderboardController.get_leaderboard(db)

@router.get("/elo/{player_id}")
async def get_elo_of_player(player_id: int, db: AsyncSession = Depends(get_db)):
    return await UserController.get_user_elo(db, player_id)