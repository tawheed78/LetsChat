import json
from pathlib import Path
from typing import Dict, List, Tuple
from fastapi import FastAPI, WebSocket
from fastapi.responses import FileResponse
from routers.authentication import router as authentication_router
from routers.add_friend import router as add_friend_router
from routers.chat_list import router as chat_list_router

from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from fastapi import WebSocket, WebSocketDisconnect
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request

from config import db


app = FastAPI()

app.mount("/static", StaticFiles(directory="frontend"), name="static")

templates = Jinja2Templates(directory="frontend")

origins = [
    "http://localhost", 
    "http://localhost:8000",
]
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("indx.html", {"request": request})

@app.get("/chat", response_class=HTMLResponse)
async def chat(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

# @app.get("/chat")
# async def serve_chat_html():
#     html_file_path = Path("frontend") / "chat.html"
#     return FileResponse(html_file_path)

# @app.get("/chat-list/")
# async def get_chat_list_page():
#     # Return the chat-list.html file as a response
#     return FileResponse("frontend/chat.html")

app.add_middleware(
    CORSMiddleware,
    # allow_origins=["*"],
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

message_collections = db['messages']

class SocketManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.chat_rooms: Dict[Tuple[str, str], List[str]] = {}

    async def connect(self, websocket: WebSocket, user: str):
        await websocket.accept()
        self.active_connections[user] = websocket

    def disconnect(self, user: str):
        if user in self.active_connections:
            del self.active_connections[user]

    async def send_personal_message(self, message: str, recipient: str):
        if recipient in self.active_connections:
            await self.active_connections[recipient].send_text(message)

    async def join_chat_room(self, user1: str, user2: str):
        room_key = tuple(sorted([user1, user2]))
        if room_key not in self.chat_rooms:
            self.chat_rooms[room_key] = []

    async def leave_chat_room(self, user1: str, user2: str):
        room_key = tuple(sorted([user1, user2]))
        if room_key in self.chat_rooms:
            del self.chat_rooms[room_key]

    async def broadcast(self, message: str, sender: str, recipient: str):
        room_key = tuple(sorted([sender, recipient]))
        if room_key in self.chat_rooms:
            room_users = self.chat_rooms[room_key]
            for user in room_users:
                await self.send_personal_message(message, user)

manager = SocketManager()
connections: Dict[WebSocket, str] = {}

@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await websocket.accept()
    connections[websocket] = username  # Track the WebSocket connection with the associated username
    try:
        while True:
            data = await websocket.receive_text()
            recipient = websocket.query_params.get("recipient")
            message = {
                "from": username,
                "to": recipient,
                "data_received": data,
                "timestamp": datetime.utcnow()
            }
            await message_collections.insert_one(message)
            recipient = websocket.query_params.get("recipient")  # Get the recipient from the query parameter
            if recipient:
                # Find the WebSocket associated with the recipient and send the message
                for ws, user in connections.items():
                    if user == recipient:
                        await ws.send_text(f"{username}: {data}")  # Send the message to the recipient
                        message = {
                            "to": recipient,
                            "from":username,
                            "data_sent": data,
                            "timestamp": datetime.utcnow()
                        }
                        await message_collections.insert_one(message)
                        
    except WebSocketDisconnect:
        connections.pop(websocket)



app.include_router(authentication_router)

app.include_router(add_friend_router)

app.include_router(chat_list_router)

