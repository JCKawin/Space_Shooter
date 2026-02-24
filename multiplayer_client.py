"""
+--------------------------------------------------------------------------------------+
|                              SPACE SHOOTER - MULTIPLAYER CLIENT                      |
|                                Team: இனிழ் (Inizh)                                  |
|                                                                                      |
|  Client module to connect game to the multiplayer server.                            |
|  Import and use this in your game to enable multiplayer features.                    |
+--------------------------------------------------------------------------------------+
"""

import asyncio
import json
import threading
import websockets
from queue import Queue
import uuid


class MultiplayerClient:
    def __init__(self, server_url: str = "ws://localhost:8000/ws"):
        self.server_url = server_url
        self.player_id = str(uuid.uuid4())[:8]  # Short unique ID
        self.websocket = None
        self.connected = False
        self.game_active = False
        
        # Queues for thread-safe communication
        self.incoming_messages = Queue()
        self.outgoing_messages = Queue()
        
        # Callbacks (set these in your game)
        self.on_game_start = None       # Called when multiplayer game starts
        self.on_game_over = None        # Called when game ends (winner/loser info)
        self.on_opponent_score = None   # Called when opponent score updates
        self.on_opponent_health = None  # Called when opponent health updates
        self.on_player_joined = None    # Called when a player joins
        self.on_player_left = None      # Called when a player leaves
        
        self._running = False
        self._thread = None
        self._loop = None

    def connect(self, player_name: str = None):
        """Start connection to server in background thread"""
        if player_name:
            self.player_id = player_name
        
        self._running = True
        self._thread = threading.Thread(target=self._run_async_loop, daemon=True)
        self._thread.start()
        print(f"Connecting to multiplayer server as {self.player_id}...")

    def disconnect(self):
        """Disconnect from server"""
        self._running = False
        if self._loop:
            self._loop.call_soon_threadsafe(self._loop.stop)

    def _run_async_loop(self):
        """Run the async event loop in a separate thread"""
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        self._loop.run_until_complete(self._connect_and_listen())

    async def _connect_and_listen(self):
        """Connect to WebSocket and listen for messages"""
        uri = f"{self.server_url}/{self.player_id}"
        
        try:
            async with websockets.connect(uri) as websocket:
                self.websocket = websocket
                self.connected = True
                print(f"Connected to server as {self.player_id}")
                
                # Create tasks for sending and receiving
                receive_task = asyncio.create_task(self._receive_messages())
                send_task = asyncio.create_task(self._send_messages())
                
                await asyncio.gather(receive_task, send_task)
                
        except Exception as e:
            print(f"Connection error: {e}")
            self.connected = False

    async def _receive_messages(self):
        """Receive messages from server"""
        while self._running and self.websocket:
            try:
                message = await self.websocket.recv()
                data = json.loads(message)
                self.incoming_messages.put(data)
            except websockets.ConnectionClosed:
                self.connected = False
                break
            except Exception as e:
                print(f"Receive error: {e}")
                break

    async def _send_messages(self):
        """Send messages from queue to server"""
        while self._running and self.websocket:
            try:
                if not self.outgoing_messages.empty():
                    message = self.outgoing_messages.get_nowait()
                    await self.websocket.send(json.dumps(message))
                else:
                    await asyncio.sleep(0.01)
            except Exception as e:
                print(f"Send error: {e}")
                break

    def _queue_message(self, message: dict):
        """Add message to outgoing queue"""
        self.outgoing_messages.put(message)

    # === Game Actions ===
    
    def start_game(self):
        """Request to start multiplayer game"""
        self._queue_message({"type": "start_game"})

    def send_death(self):
        """Notify server that this player died"""
        self._queue_message({"type": "player_died"})
        self.game_active = False

    def send_score(self, score: int):
        """Send score update to server"""
        self._queue_message({"type": "update_score", "score": score})

    def send_health(self, health: int):
        """Send health update to server"""
        self._queue_message({"type": "update_health", "health": health})

    def send_chat(self, message: str):
        """Send chat message"""
        self._queue_message({"type": "chat", "message": message})

    # === Call this in your game loop ===
    
    def update(self):
        """
        Process incoming messages - call this in your game loop!
        Returns list of events that occurred.
        """
        events = []
        
        while not self.incoming_messages.empty():
            data = self.incoming_messages.get_nowait()
            msg_type = data.get("type")
            events.append(data)
            
            if msg_type == "game_start":
                self.game_active = True
                if self.on_game_start:
                    self.on_game_start(data.get("players", []))
            
            elif msg_type == "game_over":
                self.game_active = False
                if self.on_game_over:
                    winner = data.get("winner")
                    loser = data.get("loser")
                    i_won = winner == self.player_id
                    self.on_game_over(i_won, winner, loser)
            
            elif msg_type == "opponent_score":
                if self.on_opponent_score:
                    self.on_opponent_score(data.get("player_id"), data.get("score"))
            
            elif msg_type == "opponent_health":
                if self.on_opponent_health:
                    self.on_opponent_health(data.get("player_id"), data.get("health"))
            
            elif msg_type == "player_joined":
                if self.on_player_joined:
                    self.on_player_joined(data.get("player_id"), data.get("player_count"))
            
            elif msg_type == "player_left":
                if self.on_player_left:
                    self.on_player_left(data.get("player_id"), data.get("player_count"))
        
        return events


# === Example usage in your game ===
if __name__ == "__main__":
    # Quick test
    import time
    
    client = MultiplayerClient()
    
    # Set up callbacks
    def on_game_start(players):
        print(f"Game started with players: {players}")
    
    def on_game_over(i_won, winner, loser):
        if i_won:
            print("YOU WIN!")
        else:
            print(f"YOU LOSE! Winner: {winner}")
    
    client.on_game_start = on_game_start
    client.on_game_over = on_game_over
    
    # Connect
    client.connect("TestPlayer")
    
    # Simulate game loop
    print("Running... Press Ctrl+C to stop")
    try:
        while True:
            events = client.update()
            for event in events:
                print(f"Event: {event}")
            time.sleep(0.1)
    except KeyboardInterrupt:
        client.disconnect()
        print("Disconnected")
