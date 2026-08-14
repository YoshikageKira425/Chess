from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.database import get_db
from src.controller.auth_controller import AuthController
from src.schema.auth_schema import AuthRequest

router = APIRouter()


@router.post("/login")
async def login(data: AuthRequest, db: AsyncSession = Depends(get_db)):
    user = await AuthController.login(
        db, 
        data.username,
        data.password
    )
    
    if user is None:
        raise HTTPException(
            status_code=401, detail="Invalid username or password")

    return {"id": user.id, "username": user.username, "elo": user.elo}


@router.post("/signup")
async def signup(data: AuthRequest, db: AsyncSession = Depends(get_db)):
    user = await AuthController.signup(
        db, 
        data.username, 
        data.password
    )
    
    if user is None:
        raise HTTPException(
            status_code=400, detail="Username taken or invalid input")

    return {"id": user.id, "username": user.username}
