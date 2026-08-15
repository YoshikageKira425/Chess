import asyncio
from fastapi import WebSocket


class MatchmakingQueue:
    def __init__(self):
        self._waiting: list[tuple[int, WebSocket, asyncio.Future]] = []
        self._lock = asyncio.Lock()

    async def join(self, player_id: int, websocket: WebSocket) -> tuple | None:
        async with self._lock:
            if self._waiting:
                opponent_id, opponent_ws, future = self._waiting.pop(0)
                future.cancel()  # wake up the waiting player
                return (opponent_id, opponent_ws)
            else:
                future = asyncio.get_event_loop().create_future()
                self._waiting.append((player_id, websocket, future))
                return None

    async def leave(self, player_id: int):
        async with self._lock:
            self._waiting = [(pid, ws, f) for pid, ws, f in self._waiting if pid != player_id]


matchmaking_queue = MatchmakingQueue()