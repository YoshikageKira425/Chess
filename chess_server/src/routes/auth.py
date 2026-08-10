from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.database import get_db
from src.controller.auth_controller import AuthController

router = APIRouter()

@router.post("/login")
async def login(username: str, password: str, db: AsyncSession = Depends(get_db)):
    user = await AuthController.login(db, username, password)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    return {"id": user.id, "username": user.username, "elo": user.elo}

@router.post("/signup")
async def signup(username: str, password: str, db: AsyncSession = Depends(get_db)):
    user = await AuthController.signup(db, username, password)
    if user is None:
        raise HTTPException(status_code=400, detail="Username taken or invalid input")
    
    return {"id": user.id, "username": user.username}