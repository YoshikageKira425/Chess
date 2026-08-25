import asyncio
from fastapi import WebSocket
from chess_core.enum.game_type import GameType


class MatchmakingQueue:
    def __init__(self):
        self._queues: dict[GameType, list[tuple[int, WebSocket, asyncio.Task]]] = {
            GameType.CASUAL: [],
            GameType.RANKED: [],
        }
        self._paired: dict[int, tuple[int, WebSocket]] = {}
        self._lock = asyncio.Lock()

    async def join(self, player_id: int, game_type: GameType, websocket: WebSocket) -> tuple | None:
        async with self._lock:
            queue = self._queues[game_type]

            if queue:
                opponent_id, opponent_ws, task = queue.pop(0)
                if opponent_id == player_id:
                    return None
                
                self._paired[player_id] = (opponent_id, opponent_ws)
                self._paired[opponent_id] = (player_id, websocket)
                
                task.cancel()
                return (opponent_id, opponent_ws)
            else:
                task = asyncio.current_task()
                queue.append((player_id, websocket, task))
                return None

    def get_opponent(self, player_id: int) -> tuple | None:
        return self._paired.pop(player_id, None)

    async def leave(self, player_id: int):
        async with self._lock:
            for queue in self._queues.values():
                for entry in queue:
                    if entry[0] == player_id:
                        queue.remove(entry)
                        return


matchmaking_queue = MatchmakingQueue()
