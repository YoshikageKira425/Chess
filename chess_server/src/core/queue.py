import asyncio
from fastapi import WebSocket
from chess_core.enum.game_type import GameType


class MatchmakingQueue:
    def __init__(self):
        self._queues: dict[GameType, list[tuple[int, WebSocket, asyncio.Future]]] = {
            GameType.CASUAL: [],
            GameType.RANKED: [],
        }
        self._lock = asyncio.Lock()

    async def join(self, player_id: int, game_type: GameType, websocket: WebSocket) -> tuple | None:
        async with self._lock:
            queue = self._queues[game_type]

            if queue:
                opponent_id, opponent_ws, future = queue.pop(0)
                future.cancel()
                return (opponent_id, opponent_ws)
            else:
                future = asyncio.get_event_loop().create_future()
                queue.append((player_id, websocket, future))
                return None

    async def leave(self, player_id: int):
        async with self._lock:
            for queue in self._queues.values():
                for entry in queue:
                    if entry[0] == player_id:
                        queue.remove(entry)
                        return


matchmaking_queue = MatchmakingQueue()
