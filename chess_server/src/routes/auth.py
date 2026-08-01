from fastapi import APIRouter

router = APIRouter()

@router.post("/register")
async def register():
    return {"message": "register"}

@router.post("/login")
async def login():
    return {"message": "login"}