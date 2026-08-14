import json
import random
from fastapi import WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.queue import matchmaking_queue
from src.core.game_manager import game_manager
from src.controller.games_controller import GamesController


# Tracks which websocket belongs to which game
# { game_id: { player_id: websocket } }
active_connections: dict[int, dict[int, WebSocket]] = {}


async def send(ws: WebSocket, data: dict):
    await ws.send_text(json.dumps(data))


async def broadcast(game_id: int, data: dict, exclude_player: int = None):
    for player_id, ws in active_connections.get(game_id, {}).items():
        if player_id != exclude_player:
            await send(ws, data)


async def game_socket(websocket: WebSocket, player_id: int, db: AsyncSession):
    await websocket.accept()

    # --- MATCHMAKING ---
    opponent = await matchmaking_queue.join(player_id, websocket)

    if opponent is None:
        # Waiting for opponent
        await send(websocket, {"type": "waiting"})
        try:
            # Just keep the connection alive while waiting
            while True:
                msg = await websocket.receive_text()
                if msg == "cancel":
                    await matchmaking_queue.leave(player_id)
                    await send(websocket, {"type": "cancelled"})
                    return
        except WebSocketDisconnect:
            await matchmaking_queue.leave(player_id)
            return

    # --- MATCH FOUND ---
    opponent_id, opponent_ws = opponent

    # Randomly assign colors
    if random.random() > 0.5:
        white_id, black_id = player_id, opponent_id
        white_ws, black_ws = websocket, opponent_ws
    else:
        white_id, black_id = opponent_id, player_id
        white_ws, black_ws = opponent_ws, websocket

    # Create game in DB and in-memory board
    game = await GamesController.create(db, white_id, black_id)
    game_id = game.id

    # Register connections
    active_connections[game_id] = {
        white_id: white_ws,
        black_id: black_ws,
    }

    # Notify both players
    await send(white_ws, {
        "type": "match_found",
        "game_id": game_id,
        "color": "white",
        "opponent_id": black_id,
    })
    await send(black_ws, {
        "type": "match_found",
        "game_id": game_id,
        "color": "black",
        "opponent_id": white_id,
    })

    try:
        while True:
            data = json.loads(await websocket.receive_text())

            if data["type"] == "move":
                from_pos = tuple(data["from"])
                to_pos = tuple(data["to"])

                result = await GamesController.add_move(db, game_id, from_pos, to_pos, player_id)

                if not result["success"]:
                    await send(websocket, {"type": "error", "reason": result["reason"]})
                    continue

                await broadcast(game_id, {
                    "type": "move",
                    "from": from_pos,
                    "to": to_pos,
                    "status": result["status"],
                }, exclude_player=player_id)

                if result["status"] in ("checkmate", "stalemate"):
                    await send(websocket, {"type": "game_over", "status": result["status"]})
                    active_connections.pop(game_id, None)
                    return

            elif data["type"] == "resign":
                await GamesController.end(db, game_id, winner_id=opponent_id)
                await broadcast(game_id, {"type": "game_over", "status": "resign", "winner_id": opponent_id})
                active_connections.pop(game_id, None)
                return

    except WebSocketDisconnect:
        await broadcast(game_id, {"type": "opponent_disconnected"}, exclude_player=player_id)
        active_connections.pop(game_id, None)