from fastapi import APIRouter, WebSocket, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.database import get_db
from src.routes.websocket import game_socket
from chess_core.enum.game_type import GameType

router = APIRouter()

@router.websocket("/ws/casual/{player_id}")
async def casual_match(websocket: WebSocket, player_id: int, db: AsyncSession = Depends(get_db)):
    await game_socket(websocket, player_id, GameType.CASUAL, db)
    
@router.websocket("/ws/ranked/{player_id}")
async def ranked_match(websocket: WebSocket, player_id: int, db: AsyncSession = Depends(get_db)):
    await game_socket(websocket, player_id, GameType.RANKED, db)