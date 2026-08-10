from fastapi import APIRouter, WebSocket, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.database import get_db
from src.routes.websocket import game_socket

router = APIRouter()

@router.websocket("/ws/{player_id}")
async def websocket_endpoint(websocket: WebSocket, player_id: int, db: AsyncSession = Depends(get_db)):
    await game_socket(websocket, player_id, db)