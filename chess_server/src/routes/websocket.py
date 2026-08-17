import json
import random
import asyncio
from fastapi import WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.queue import matchmaking_queue
from src.core.game_manager import game_manager
from src.controller.games_controller import GamesController
from src.controller.user_controller import UserController
from chess_core.enum.color_enum import Color

active_connections: dict[int, dict[int, WebSocket]] = {}


async def send(ws: WebSocket, data: dict):
    await ws.send_text(json.dumps(data))


async def broadcast(game_id: int, data: dict, exclude_player: int = None):
    for player_id, ws in active_connections.get(game_id, {}).items():
        if player_id != exclude_player:
            await send(ws, data)


async def handle_player(websocket: WebSocket, player_id: int, opponent_id: int, game_id: int, db: AsyncSession):
    """Handles the game loop for a single player."""
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
                    await broadcast(game_id, {
                        "type": "game_over",
                        "status": result["status"],
                        "winner_id": result.get("winner_id")
                    })
                    
                    if result["status"] == "checkmate":
                        loser_id = opponent_id if player_id == result.get("winner_id") else player_id
                        await finish_game(db, result.get("winner_id"), loser_id)
                    
                    active_connections.pop(game_id, None)
                    return

            elif data["type"] == "resign":
                await GamesController.end(db, game_id, winner_id=opponent_id)
                await broadcast(game_id, {
                    "type": "game_over",
                    "status": "resign",
                    "winner_id": opponent_id
                })
                
                await finish_game(db, opponent_id, player_id)
                                    
                active_connections.pop(game_id, None)
                return

    except WebSocketDisconnect:
        await broadcast(game_id, {"type": "opponent_disconnected"}, exclude_player=player_id)
        await finish_game(db, opponent_id, player_id)
                        
        active_connections.pop(game_id, None)


async def game_socket(websocket: WebSocket, player_id: int, db: AsyncSession):
    await websocket.accept()

    opponent = await matchmaking_queue.join(player_id, websocket)

    if opponent is None:
        # Waiting — send waiting message and hold until opponent joins
        await send(websocket, {"type": "waiting"})

        # Wait until this player gets paired (queue will handle it)
        # The connection stays open — the opponent's join() will find us
        try:
            await asyncio.Future()
        except asyncio.CancelledError:
            pass
        except WebSocketDisconnect:
            await matchmaking_queue.leave(player_id)
            return

    opponent_id, opponent_ws = opponent

    if random.random() > 0.5:
        white_id, black_id = player_id, opponent_id
        white_ws, black_ws = websocket, opponent_ws
    else:
        white_id, black_id = opponent_id, player_id
        white_ws, black_ws = opponent_ws, websocket

    game = await GamesController.create(db, white_id, black_id)
    game_id = game.id

    active_connections[game_id] = {
        white_id: white_ws,
        black_id: black_ws,
    }

    await send(white_ws, {
        "type": "match_found",
        "game_id": game_id,
        "color": Color.WHITE,
        "opponent_id": black_id,
    })
    await send(black_ws, {
        "type": "match_found",
        "game_id": game_id,
        "color": Color.BLACK,
        "opponent_id": white_id,
    })

    await asyncio.gather(
        handle_player(white_ws, white_id, black_id, game_id, db),
        handle_player(black_ws, black_id, white_id, game_id, db),
    )


async def finish_game(
    db: AsyncSession,
    winner_id: int,
    loser_id: int,
):
    await UserController.update_elo(
        db,
        winner_id,
        10
    )

    await UserController.update_elo(
        db,
        loser_id,
        -10
    )