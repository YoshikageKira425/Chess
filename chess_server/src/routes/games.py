from fastapi import APIRouter

router = APIRouter()

@router.post("/create")
async def create_game():
    return {"message": "game created"}

@router.get("/{game_id}")
async def get_game(game_id: str):
    return {"game_id": game_id}