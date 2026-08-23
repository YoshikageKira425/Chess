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
from src.enum.game_type import GameType

active_connections: dict[int, dict[int, WebSocket]] = {}


async def send(ws: WebSocket, data: dict):
    await ws.send_text(json.dumps(data))


async def broadcast(game_id: int, data: dict, exclude_player: int = None):
    for player_id, ws in active_connections.get(game_id, {}).items():
        if player_id != exclude_player:
            await send(ws, data)


async def handle_player(websocket: WebSocket, player_id: int, opponent_id: int, game_id: int, db: AsyncSession):
    """Handles the game loop for a single player."""
    MOVE_TIMEOUT = 60.0

    try:
        while True:
            try:
                raw = await asyncio.wait_for(
                    websocket.receive_text(),
                    timeout=MOVE_TIMEOUT
                )
            except asyncio.TimeoutError:
                await ending_match(db, game_id, opponent_id, player_id, "timeout")
                return

            data = json.loads(raw)

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
                    loser_id = opponent_id if player_id == result.get(
                        "winner_id") else player_id
                    await ending_match(db, game_id, result.get("winner_id"), loser_id, result["status"])

                    return

            elif data["type"] == "resign":
                await ending_match(db, game_id, opponent_id, player_id, "resign")
                return

    except WebSocketDisconnect:
        await ending_match(db, game_id, opponent_id, player_id, "resign", "opponent_disconnected")


async def game_socket(websocket: WebSocket, player_id: int, db: AsyncSession):
    await websocket.accept()

    opponent = await matchmaking_queue.join(player_id, websocket)

    if opponent is None:
        await send(websocket, {"type": "waiting"})

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

    game = await GamesController.create(db, white_id, black_id, GameType.CASUAL)
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


async def ending_match(
    db: AsyncSession,
    game_id: int,
    winner_id: int,
    loser_id: int,
    status: str,
    type: str = "game_over"
):
    await broadcast(game_id, {
        "type": type,
        "status": status,
        "winner_id": winner_id
    })
    await GamesController.end(db, game_id, winner_id=winner_id)

    if status in ["checkmate", "resign", "timeout"]:
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

    active_connections.pop(game_id, None)
