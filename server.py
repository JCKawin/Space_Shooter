from typing import list

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel


class ClientData(BaseModel):
    client_id: str
    data: str


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        await self.broadcast(f"Client {websocket.client_id} connected")

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        await self.broadcast(f"Client {websocket.client_id} disconnected")

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


app = FastAPI()

manager = ConnectionManager()


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):

    try:
        await manager.connect(websocket)
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Message from {client_id}: {data}")

    except WebSocketDisconnect:
        await manager.disconnect(websocket)
