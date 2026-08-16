import asyncio
import json
import threading
from queue import Queue
import websockets

class NetworkManager:
    def __init__(self, player_id: int):
        self.player_id = player_id
        self.url = f"ws://localhost:8000/game/ws/{player_id}"

        self.websocket = None
        self.events = Queue()

        self.color = None
        self.game_id = None

        self._loop = asyncio.new_event_loop()
        self._thread = threading.Thread(
            target=self._run,
            daemon=True,
        )

        self._thread.start()

    def _run(self):
        asyncio.set_event_loop(self._loop)
        self._loop.run_until_complete(self._connect())

    async def _connect(self):
        try:
            async with websockets.connect(self.url) as websocket:
                self.websocket = websocket

                async for message in websocket:
                    self.events.put(json.loads(message))
        except:
            print("Failed to connect to the websocket!")
        finally:
            self.websocket = None

    def send_move(
        self,
        from_pos: tuple,
        to_pos: tuple,
    ):
        self._send({
            "type": "move",
            "from": from_pos,
            "to": to_pos,
        })

    def resign(self):
        self._send({
            "type": "resign",
        })

    def _send(self, data: dict):
        if self.websocket is None:
            print("Cannot send: WebSocket is not connected")
            return

        asyncio.run_coroutine_threadsafe(
            self._send_async(data),
            self._loop,
        )

    async def _send_async(self, data: dict):
        await self.websocket.send(json.dumps(data))
