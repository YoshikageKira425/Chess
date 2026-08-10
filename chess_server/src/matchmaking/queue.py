import asyncio
from fastapi import WebSocket


class MatchmakingQueue:
    def __init__(self):
        self._waiting: list[tuple[int, WebSocket]] = []  
        self._lock = asyncio.Lock()

    async def join(self, player_id: int, websocket: WebSocket) -> tuple | None:
        async with self._lock:
            if self._waiting:
                opponent_id, opponent_ws = self._waiting.pop(0)
                return (opponent_id, opponent_ws)  
            else:
                self._waiting.append((player_id, websocket))
                return None

    async def leave(self, player_id: int):
        async with self._lock:
            self._waiting = [(pid, ws) for pid, ws in self._waiting if pid != player_id]


matchmaking_queue = MatchmakingQueue()