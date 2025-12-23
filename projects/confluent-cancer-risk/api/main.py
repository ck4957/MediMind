from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import logging
from typing import List
import json
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.consumer_service import KafkaConsumerService
from api.mock_service import MockDataService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api")

app = FastAPI(title="Cancer Risk Assessment API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For hackathon/dev allow all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global services
consumer_service = KafkaConsumerService()
mock_service = MockDataService()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                logger.error(f"Error sending message: {e}")

manager = ConnectionManager()

@app.on_event("startup")
async def startup_event():
    # Start consumer service in background
    asyncio.create_task(consumer_service.start(message_callback=manager.broadcast))
    logger.info("Application started")

@app.on_event("shutdown")
async def shutdown_event():
    await consumer_service.stop()

@app.get("/")
def read_root():
    return {"status": "online", "service": "Cancer Risk Assessment API"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive, maybe wait for client commands
            data = await websocket.receive_text()
            # For now, we just echo or ignore client messages
            # In a real app, this could be used to subscribe to specific patient IDs
    except WebSocketDisconnect:
        manager.disconnect(websocket)
