from fastapi import APIRouter,  Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.database import get_db
from src.controller.leaderboard_controller import LeaderboardController

router = APIRouter()

@router.get("/")
async def get_leaderboard(db: AsyncSession = Depends(get_db)):
    return await LeaderboardController.get_leaderboard(db)