import asyncio
import websockets
import json
import threading


class NetworkManager:
    def __init__(self, player_id: int, server_url: str = "ws://localhost:8000"):
        self.player_id = player_id
        self.url = f"{server_url}/game/ws/{player_id}"
        self.websocket = None
        self.color = None
        self.game_id = None

        self.on_match_found = None
        self.on_move_received = None
        self.on_game_over = None
        self.on_opponent_disconnected = None

        self._thread = threading.Thread(target=self._run, daemon=True)
        self._loop = asyncio.new_event_loop()
        self._thread.start()

    def _run(self):
        asyncio.set_event_loop(self._loop)
        self._loop.run_until_complete(self._connect())

    async def _connect(self):
        try:
            async with websockets.connect(self.url) as ws:
                self.websocket = ws
                async for message in ws:
                    data = json.loads(message)
                    self._handle(data)
        except:
            print("Failed to connect to the websocket!")            
        
    def _handle(self, data: dict):
        t = data.get("type")
        if t == "match_found":
            self.color = data["color"]
            self.game_id = data["game_id"]
            if self.on_match_found:
                self.on_match_found(data)
        elif t == "move":
            if self.on_move_received:
                self.on_move_received(data["from"], data["to"])
        elif t == "game_over":
            if self.on_game_over:
                self.on_game_over(data)
        elif t == "opponent_disconnected":
            if self.on_opponent_disconnected:
                self.on_opponent_disconnected()

    def send_move(self, from_pos: tuple, to_pos: tuple):
        asyncio.run_coroutine_threadsafe(
            self._send({"type": "move", "from": from_pos, "to": to_pos}),
            self._loop
        )

    def resign(self):
        asyncio.run_coroutine_threadsafe(
            self._send({"type": "resign"}),
            self._loop
        )

    async def _send(self, data: dict):
        if self.websocket:
            await self.websocket.send(json.dumps(data))
