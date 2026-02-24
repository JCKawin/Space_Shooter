"""
+--------------------------------------------------------------------------------------+
|                              SPACE SHOOTER - MULTIPLAYER SERVER                      |
|                                Team: இனிழ் (Inizh)                                  |
|                                                                                      |
|  A simple FastAPI WebSocket server for multiplayer Space Shooter game.               |
|  Handles player connections, game start sync, and game-over notifications.           |
+--------------------------------------------------------------------------------------+
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import Dict, List
import json
import asyncio
import uvicorn

app = FastAPI(title="Space Shooter Multiplayer Server")

# Store connected players
class GameRoom:
    def __init__(self):
        self.players: Dict[str, WebSocket] = {}
        self.game_active: bool = False
        self.winner: str | None = None
    
    async def connect(self, player_id: str, websocket: WebSocket):
        await websocket.accept()
        self.players[player_id] = websocket
        await self.broadcast({
            "type": "player_joined",
            "player_id": player_id,
            "player_count": len(self.players)
        })
        print(f"Player {player_id} connected. Total players: {len(self.players)}")
    
    def disconnect(self, player_id: str):
        if player_id in self.players:
            del self.players[player_id]
            print(f"Player {player_id} disconnected. Total players: {len(self.players)}")
    
    async def broadcast(self, message: dict, exclude: str = None):
        """Send message to all connected players"""
        for player_id, websocket in self.players.items():
            if player_id != exclude:
                try:
                    await websocket.send_json(message)
                except:
                    pass
    
    async def send_to_player(self, player_id: str, message: dict):
        """Send message to a specific player"""
        if player_id in self.players:
            try:
                await self.players[player_id].send_json(message)
            except:
                pass

# Global game room (for simplicity, single room)
game_room = GameRoom()


@app.get("/")
async def root():
    return {
        "message": "Space Shooter Multiplayer Server",
        "status": "running",
        "players_online": len(game_room.players)
    }


@app.websocket("/ws/{player_id}")
async def websocket_endpoint(websocket: WebSocket, player_id: str):
    await game_room.connect(player_id, websocket)
    
    try:
        while True:
            # Receive message from player
            data = await websocket.receive_json()
            message_type = data.get("type")
            
            if message_type == "start_game":
                # Player wants to start multiplayer game
                if len(game_room.players) >= 2:
                    game_room.game_active = True
                    game_room.winner = None
                    await game_room.broadcast({
                        "type": "game_start",
                        "message": "Multiplayer game starting!",
                        "players": list(game_room.players.keys())
                    })
                    print("Game started with players:", list(game_room.players.keys()))
                else:
                    await game_room.send_to_player(player_id, {
                        "type": "error",
                        "message": "Need at least 2 players to start multiplayer"
                    })
            
            elif message_type == "player_died":
                # A player has died - other player wins
                if game_room.game_active:
                    game_room.game_active = False
                    
                    # Find the winner (the other player who didn't die)
                    for pid in game_room.players.keys():
                        if pid != player_id:
                            game_room.winner = pid
                            break
                    
                    # Notify all players about game end
                    await game_room.broadcast({
                        "type": "game_over",
                        "loser": player_id,
                        "winner": game_room.winner,
                        "message": f"Player {player_id} died! {game_room.winner} wins!"
                    })
                    print(f"Game Over! Winner: {game_room.winner}, Loser: {player_id}")
            
            elif message_type == "update_score":
                # Broadcast score updates to other players
                await game_room.broadcast({
                    "type": "opponent_score",
                    "player_id": player_id,
                    "score": data.get("score", 0)
                }, exclude=player_id)
            
            elif message_type == "update_health":
                # Broadcast health updates to other players
                await game_room.broadcast({
                    "type": "opponent_health",
                    "player_id": player_id,
                    "health": data.get("health", 100)
                }, exclude=player_id)
            
            elif message_type == "ping":
                # Simple ping-pong for connection check
                await game_room.send_to_player(player_id, {"type": "pong"})
            
            elif message_type == "chat":
                # Simple chat message relay
                await game_room.broadcast({
                    "type": "chat",
                    "player_id": player_id,
                    "message": data.get("message", "")
                })
    
    except WebSocketDisconnect:
        game_room.disconnect(player_id)
        
        # If game was active and a player disconnects, other player wins
        if game_room.game_active and len(game_room.players) > 0:
            game_room.game_active = False
            remaining_player = list(game_room.players.keys())[0]
            game_room.winner = remaining_player
            await game_room.broadcast({
                "type": "game_over",
                "loser": player_id,
                "winner": remaining_player,
                "message": f"Player {player_id} disconnected! {remaining_player} wins!"
            })
        
        await game_room.broadcast({
            "type": "player_left",
            "player_id": player_id,
            "player_count": len(game_room.players)
        })
    
    except Exception as e:
        print(f"Error with player {player_id}: {e}")
        game_room.disconnect(player_id)


if __name__ == "__main__":
    print("=" * 60)
    print("       SPACE SHOOTER - MULTIPLAYER SERVER")
    print("=" * 60)
    print("Starting server on http://localhost:8000")
    print("WebSocket endpoint: ws://localhost:8000/ws/{player_id}")
    print("=" * 60)
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
